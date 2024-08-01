"""Asynchronous Python client for Lektrico device."""
from __future__ import annotations

from builtins import float
from pydantic.v1 import BaseModel


class Info(BaseModel):
    """Object holding the Lektrico device information.
    """
    current_l1: float
    current_l2: float
    current_l3: float
    voltage_l1: float
    voltage_l2: float
    voltage_l3: float
    fw_version: str
    

class InfoForCharger(Info):
    """Object holding the Lektrico charger information.
    """
    charger_state: str
    charging_time: int
    contactor_failure: bool
    cp_diode_failure: bool
    critical_temp: bool
    current_limit_reason: str
    dynamic_current: int
    has_active_errors: bool
    install_current: int
    instant_power: float
    led_max_brightness: int
    meter_fault: bool
    overcurrent: bool
    overtemp: bool
    overvoltage_error: bool
    relay_mode: int
    require_auth: bool
    rcd_error: bool
    temperature: float
    total_charged_energy: float
    session_energy: float
    state_e_activated: bool
    undervoltage_error: bool
    user_current: int


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


class Settings(BaseModel):
    """Object holding the Lektrico device settings.
    """
    type: str
    serial_number: int
    board_revision: str
    