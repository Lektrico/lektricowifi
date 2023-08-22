"""Asynchronous Python client for Lektrico device."""
from __future__ import annotations

from builtins import float
from pydantic import BaseModel


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
    