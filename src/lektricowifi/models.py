"""Asynchronous Python client for Lektrico charger."""
from __future__ import annotations

from dataclasses import dataclass
from builtins import float


@dataclass
class Info:
    """Object holding the Lektrico charger information.
    """
    charger_state: str
    session_energy: float
    charging_time: int
    instant_power: float
    current: float
    voltage: float
    temperature: float
    dynamic_current: int
    require_auth: bool
    install_current: int
    led_max_brightness: int
    total_charged_energy: int
    fw_version: str
    has_active_errors: bool
    state_e_activated: bool
    overtemp: bool
    critical_temp: bool
    overcurrent: bool
    meter_fault: bool
    voltage_error: bool
    rcd_error: bool
    user_current: int

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Info:
        """Return an Info object from a Lektrico charger response.
        """
        
        return Info(
            charger_state=data["extended_charger_state"],
            session_energy=data["session_energy"],
            charging_time=data["charging_time"],
            instant_power=data["instant_power"],
            current=data["current"],
            voltage=data["voltage"],
            temperature=data["temperature"],
            dynamic_current = data["dynamic_current"],
            require_auth = not data["headless"],
            install_current = data["install_current"],
            led_max_brightness = data["led_max_brightness"],
            total_charged_energy = data["total_charged_energy"],
            fw_version = data["fw_version"],
            has_active_errors = data["has_active_errors"],
            state_e_activated = data["state_e_activated"],
            overtemp = data["overtemp"],
            critical_temp = data["critical_temp"],
            overcurrent = data["overcurrent"],
            meter_fault = data["meter_fault"],
            voltage_error = data["voltage_error"],
            rcd_error = data["rcd_error"],
            user_current = data["user_current"]
        )


@dataclass
class Settings:
    """Object holding the Lektrico charger settings.
    """
    overtemp_threshold: int
    critical_temp_threshold: int
    voltage_gain: float
    current_gain: float 
    calibration_temperature: float
    rcd_enabled: bool
    serial_number: int
    board_revision: str
    temp_offset: float

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Settings:
        """Return a Settings object from a Lektrico charger response.
        """
        return Settings(
            overtemp_threshold=data["overtemp_threshold"],
            critical_temp_threshold=data["critical_temp_threshold"],
            voltage_gain=data["voltage_gain"],
            current_gain=data.get("current_gain"),
            calibration_temperature=data.get("calibration_temperature"),
            rcd_enabled=data.get("rcd_enabled"),
            serial_number=data["serial_number"],
            board_revision=data["board_revision"],
            temp_offset=data["temp_offset"],
        )
