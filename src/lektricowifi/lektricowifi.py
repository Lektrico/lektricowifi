"""Asynchronous Python client for Lektrico device."""
from __future__ import annotations

import asyncio
import socket
from dataclasses import dataclass
from importlib import metadata
from typing import Any, TypedDict

from aiohttp.client import ClientError, ClientResponseError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from .exceptions import DeviceConnectionError, DeviceError
from .models import InfoForCharger, SettingsForCharger, DetectType

from async_timeout import timeout
from builtins import str


@dataclass
class Device:
    """Main class for handling connections with a Lektrico device."""

    _host: str

    request_timeout: int = 8
    session: ClientSession | None = None

    _close_session: bool = False

    async def _request(self,uri: str) -> dict[str, Any]:
        """Handle a request to a Lektrico device.
        Args:
            uri: ex: "charger_info.get"
        Returns:
            A Python dictionary (JSON decoded) with the response from
            the Lektrico charger.
        Raises:
            DeviceConnectionError: An error occurred while communicating with
                the Lektrico device.
            DeviceError: Received an unexpected response from the Lektrico 
                device.
        """
        url = F"http://{self._host}/rpc/{uri}"
        print(url)

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with timeout(self.request_timeout):
                response = await self.session.request(
                    METH_GET,
                    url,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            raise DeviceConnectionError(
                "Timeout occurred while connecting to Lektrico device"
            ) from exception
        except (
            ClientError,
            ClientResponseError,
            socket.gaierror,
        ) as exception:
            raise DeviceConnectionError(
                "Error occurred while communicating with Lektrico device"
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            raise DeviceError(
                "Unexpected response from the Lektrico device",
                {"Content-Type": content_type, "response": text},
            )

        return await response.json()

    async def charger_info(self) -> InfoForCharger:
        """ Get information from Lektrico charger
        {'charger_state': 'A', 'session_energy': 0.0, 'charging_time': 0, 
        'session_id': 13, 'instant_power': 0.0, 'current': 0.0, 'voltage': 0.0, 
        'temperature': 31.7, 'energy_index': 0.0, dynamic_current=32, 
        headless=False, install_current=32, led_max_brightness=20, 
        total_charged_energy: 0, fw_version='1.23'}
        """
        data_info = await self._request("charger_info.get")
        data_dyn = await self._request("dynamic_current.get")
        data = dict(data_info, **data_dyn)
        data_new = await self._request("app_config.get")
        data.update(data_new)
        data_new = await self._request("counters_config.get")
        data.update(data_new)
        data_new = await self._request("sw_version.get")
        data.update(data_new)
        data_new = await self._request("active_errors.get")
        data.update(data_new)
        
        # put readable format for state
        data["extended_charger_state"] = self._put_readable_format(data["extended_charger_state"])
        return InfoForCharger.from_dict(data)
    
    def _put_readable_format(self, _state: str) -> str:
        """Convert state in a readable format.
        ex: state="B_AUTH" -> "Connected_NeedAuth" """
        if _state == "A":
            return "Available"
        elif _state == "B":
            return "Connected"
        elif _state == "B_AUTH":
            return "Connected,NeedAuth"
        elif _state == "C" or _state == "D":
            return "Charging"
        elif _state == "E" or _state == "F":
            return "Error"
        elif _state == "OTA":
            return "Updating firmware"
        else:
            return _state

    async def charger_config(self) -> SettingsForCharger:
        """Returns the charger's configuration, as a string
        {'overtemp_threshold': 65, 'critical_temp_threshold': 75, 
        'voltage_gain': 1.0, 'current_gain': 1.0, 
        'calibration_temperature': 25.0, 'rcd_enabled': False, 
        'serial_number': 500006, 'board_revision': 'B', 'temp_offset': 0.0}"""
        data = await self._request("charger_config.get")
        return SettingsForCharger.from_dict(data)
    
    async def detect_device_type(self) -> DetectType:
        """Returns the device's type.
        Ex: {'type': '1p7k'}"""
        data = await self._request("Device_id.Get")
        return DetectType.from_dict(data)
    
    async def send_command(self, command: str) -> bool:
        """Returns the device's confirmation
        ex: True
        param command - examples: charge.start, charge.stop"""
        return await self._request(command)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Device:
        """Async enter.
        Returns:
            The Device object.
        """
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit.
        Args:
            _exc_info: Exec type.
        """
        await self.close()
