"""Asynchronous Python client for Lektrico device."""
from __future__ import annotations

import asyncio
import socket
from dataclasses import dataclass
from importlib import metadata
from typing import Any, TypedDict
from enum import IntEnum

from aiohttp.client import ClientError, ClientResponseError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from .exceptions import DeviceConnectionError, DeviceError
from .models import InfoForCharger, InfoForM2W, Info, Settings

from async_timeout import timeout
from builtins import str


class LBMode(IntEnum):
    """Enumeration of load balancing modes."""
    OFF = 0
    POWER = 1
    HYBRID = 2
    GREEN = 3


@dataclass
class Device:
    """Main class for handling connections with a Lektrico device."""

    _host: str
    
    TYPE_1P7K: str = "1p7k"
    TYPE_3P22K: str = "3p22k"
    TYPE_M2W: str = "m2w"
    
    CURRENT_LIMIT_REASON = ["No Limit", "Installation Current", 
                            "User Limit", "Dynamic Limit", "Schedule",
                            "EM Offline", "EM", "OCPP"]
    
    request_timeout: int = 8
    session: ClientSession | None = None

    _close_session: bool = False

    async def device_info(self, type: str) -> Info:
        """ Get information from Lektrico device.
        Ex for a charger:
        {'charger_state': 'A', 'session_energy': 0.0, 'charging_time': 0, 
        'session_id': 13, 'instant_power': 0.0, 'current': 0.0, 'voltage': 0.0, 
        'temperature': 31.7, 'energy_index': 0.0, dynamic_current=32, 
        headless=False, install_current=32, led_max_brightness=20, 
        total_charged_energy: 0, fw_version='1.23'}
        """
        if type == self.TYPE_1P7K or type == self.TYPE_3P22K:
            data_info = await self._request("charger_info.get")
            data_dyn = await self._request("app_config.get")
            data = dict(data_info, **data_dyn)
            data_new = await self._request("active_errors.get")
            data.update(data_new)
            
            # put readable format for state
            data["extended_charger_state"] = self._put_readable_format(data["extended_charger_state"])
            # put current_limit_reason as str
            data["current_limit_reason"] = self.CURRENT_LIMIT_REASON[int(data["current_limit_reason"])]
            return InfoForCharger.from_dict(data)
        elif type == self.TYPE_M2W:
            data_info = await self._request("Meter_info.Get")
            data_dyn = await self._request("App_config.Get")
            data = dict(data_info, **data_dyn)
            data_new = await self._request("Sw_version.Get")
            data.update(data_new)
            return InfoForM2W.from_dict(data)
        else:
            raise DeviceError("Unknown device_id")
    
    async def device_config(self) -> Settings:
        """Return the charger's configuration.
        Ex:
        {'type': '1p7k', 'serial_number': 500006, 'board_revision': 'B'}"""
        # get device's type
        data = await self._request("Device_id.Get")
        index: int = data["device_id"].find("_")
        if index == -1:
            raise DeviceError("Incorrect device_id. Expected: type_serialNumber")
        _type: str = data["device_id"][0:index]
        data_type: dict
        if _type == self.TYPE_1P7K or _type == self.TYPE_3P22K:
            data_type = {"type": _type}
            data = await self._request("charger_config.get")
        elif _type == self.TYPE_M2W:
            data_type = {"type": self.TYPE_M2W}
            data = await self._request("M2w_config.Get")
        else:
            raise DeviceError("Unknown device_id")
        
        data = dict(data_type, **data)
        return Settings.from_dict(data)
    
    async def send_command(self, command: str) -> bool:
        """Return the device's confirmation.
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

