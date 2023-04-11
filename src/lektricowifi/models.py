"""Asynchronous Python client for Lektrico device."""
from __future__ import annotations

from dataclasses import dataclass
from builtins import float

@dataclass
class Info:
    """Object holding the Lektrico device information.
    """
    current_l1: float
    current_l2: float
    current_l3: float
    voltage_l1: float
    voltage_l2: float
    voltage_l3: float
    fw_version: str
    

@dataclass
class InfoForCharger(Info):
    """Object holding the Lektrico charger information.
    """
    charger_state: str
    session_energy: float
    charging_time: int
    instant_power: float
    temperature: float
    dynamic_current: int
    require_auth: bool
    install_current: int
    led_max_brightness: int
    total_charged_energy: int
    has_active_errors: bool
    state_e_activated: bool
    overtemp: bool
    critical_temp: bool
    overcurrent: bool
    meter_fault: bool
    undervoltage_error: bool
    overvoltage_error: bool
    rcd_error: bool
    cp_diode_failure: bool
    contactor_failure: bool
    user_current: int
    current_limit_reason: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> InfoForCharger:
        """Return an Info object from a Lektrico charger response.
        """
        _state_e_activated: bool
        if "state_e_activated" in data.keys():
            _state_e_activated = data["state_e_activated"]
        else:
            _state_e_activated = data["state_machine_e_activated"]
        
        return InfoForCharger(
            charger_state=data["extended_charger_state"],
            session_energy=data["session_energy"],
            charging_time=data["charging_time"],
            instant_power=data["instant_power"],
            current_l1=list(data["currents"])[0],
            current_l2=list(data["currents"])[1],
            current_l3=list(data["currents"])[2],
            voltage_l1=list(data["voltages"])[0],
            voltage_l2=list(data["voltages"])[1],
            voltage_l3=list(data["voltages"])[2],
            temperature=data["temperature"],
            dynamic_current = data["dynamic_current"],
            require_auth = not data["headless"],
            install_current = data["install_current"],
            led_max_brightness = data["led_max_brightness"],
            total_charged_energy = data["total_charged_energy"],
            fw_version = data["fw_version"],
            has_active_errors = data["has_active_errors"],
            state_e_activated = _state_e_activated,
            overtemp = data["overtemp"],
            critical_temp = data["critical_temp"],
            overcurrent = data["overcurrent"],
            meter_fault = data["meter_fault"],
            undervoltage_error = data["undervoltage_error"],
            overvoltage_error = data["overvoltage_error"],
            rcd_error = data["rcd_error"],
            cp_diode_failure = data["cp_diode_failure"],
            contactor_failure = data["contactor_failure"],
            user_current = data["user_current"],
            current_limit_reason = data["current_limit_reason"]
        )


@dataclass
class InfoForM2W(Info):
    """Object holding the Lektrico load balancer device information.
    """
    power_l1: float
    power_l2: float
    power_l3: float
    breaker_curent: int
    power_factor_l1: float
    power_factor_l2: float
    power_factor_l3: float
    lb_mode: int
    
    @staticmethod
    def from_dict(data: dict[str, Any]) -> InfoForM2W:
        """Return an InfoForM2W object from a Lektrico device response.
        """
        return InfoForM2W(
            current_l1 = list(data["current"])[0],
            current_l2 = list(data["current"])[1],
            current_l3 = list(data["current"])[2],
            voltage_l1 = list(data["voltage"])[0],
            voltage_l2 = list(data["voltage"])[1],
            voltage_l3 = list(data["voltage"])[2],
            fw_version = data["fw_version"],
            power_l1 = list(data["active_p"])[0],
            power_l2 = list(data["active_p"])[1],
            power_l3 = list(data["active_p"])[2],
            breaker_curent = data["breaker_rating"],
            power_factor_l1 = list(data["power_factor"])[0],
            power_factor_l2 = list(data["power_factor"])[1],
            power_factor_l3 = list(data["power_factor"])[2],
            lb_mode = data["load_balancing_mode"]
        )

@dataclass
class Settings:
    """Object holding the Lektrico device settings.
    """
    type: str
    serial_number: int
    board_revision: str
    
    @staticmethod
    def from_dict(data: dict[str, Any]) -> Settings:
        """Return a Settings object from a Lektrico device response.
        """
        return Settings(
            type = data["type"],
            serial_number=data["serial_number"],
            board_revision=data["board_revision"]
        )
