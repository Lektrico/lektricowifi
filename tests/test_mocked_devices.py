from typing import Self
import pytest
from lektricowifi.exceptions import DeviceConnectionError
from lektricowifi.lektricowifi import Device
from lektricowifi.models import InfoForCharger, InfoForM2W, Settings
from asyncmock import AsyncMock

from tests.test_online_devices import process_for_pytest



@pytest.fixture
def mock_1p7k() -> AsyncMock:
    """
    Async Mock Fixture for 1P7K
    :return:
    """
    _device_answer_at_info = {"currents": [0.015, 0.006, 0.011],
                     "voltages": [238.53, 238.521, 236.852],
                     "fw_version": "1.45_beta", "extended_charger_state": "Available", 
                     "session_energy": 0.0, "charging_time": 0, 
                     "instant_power": 0.0, "temperature": 39.8, 
                     "dynamic_current": 32, "require_auth": False, 
                     "install_current": 6, "led_max_brightness": 100, 
                     "total_charged_energy": 18.0, "has_active_errors": False,
                     "state_e_activated": False, "overtemp": False, 
                     "critical_temp": False, "overcurrent": False, 
                     "meter_fault": False, "undervoltage_error": False, 
                     "overvoltage_error": False, "rcd_error": False, 
                     "cp_diode_failure": False, "contactor_failure": False, "headless": False,
                     "user_current": 32, "current_limit_reason": "Installation current"}
    mock_1p7k = AsyncMock()
    mock_1p7k.Device.device_info = AsyncMock(
        return_value= InfoForCharger.from_dict(_device_answer_at_info)
    )
    mock_1p7k.Device.device_config = AsyncMock(
        return_value= Settings.from_dict({"type": "1p7k", "serial_number": 500000, "board_revision": "E"})
    )
    mock_1p7k.Device.send_charge_start = AsyncMock(
        return_value= {'id': 57130362, 'src': '1p7k_500000', 'dst': 'MOCK', 'result': True}
    )
    mock_1p7k.Device.send_charge_stop = AsyncMock(
        return_value= {'id': 57130362, 'src': '1p7k_500000', 'dst': 'MOCK', 'result': True}
    )
    mock_1p7k.Device.send_reset = AsyncMock(
        return_value= {'id': 57130362, 'src': '1p7k_500000', 'dst': 'MOCK', 'result': True}
    )
    mock_1p7k.Device.set_auth = AsyncMock(
        return_value= {'id': 57130362, 'src': '1p7k_500000', 'dst': 'MOCK', 'result': True}
    )
    mock_1p7k.Device.set_led_max_brightness = AsyncMock(
        return_value= {'id': 57130362, 'src': '1p7k_500000', 'dst': 'MOCK', 'result': True}
    )
    mock_1p7k.Device.set_dynamic_current = AsyncMock(
        return_value= {'id': 57130362, 'src': '1p7k_500000', 'dst': 'MOCK', 'result': True}
    )
    mock_1p7k.Device.set_user_current = AsyncMock(
        return_value= {'id': 57130362, 'src': '1p7k_500000', 'dst': 'MOCK', 'result': True}
    )
    mock_1p7k.Device.set_charger_locked = AsyncMock(
        return_value= {'id': 57130362, 'src': '1p7k_500000', 'dst': 'MOCK', 'result': True}
    )

    return mock_1p7k


@pytest.fixture
def mock_em() -> AsyncMock:
    """
    Async Mock Fixture for EM
    :return:
    """
    _device_answer_at_info = {"current": [0.015, 0.006, 0.011],
                     "voltage": [238.53, 238.521, 236.852],
                     "active_p": [0.0, 0.0, 0.0],
                     "fw_version": "1.15", "breaker_rating": 32, 
                     "power_factor": [0.0, 0.0, 0.0], "load_balancing_mode": 0}
    
    mock_em = AsyncMock()
    mock_em.Device.device_info = AsyncMock(
        return_value= InfoForM2W.from_dict(_device_answer_at_info)
    )
    mock_em.Device.device_config = AsyncMock(
        return_value= Settings.from_dict({"type": "em", "serial_number": 800000, "board_revision": "A"})
    )
    mock_em.Device.send_reset = AsyncMock(
        return_value= {'id': 57130362, 'src': 'm2w_800000', 'dst': 'MOCK', 'result': True}
    )
    mock_em.Device.set_load_balancing_mode = AsyncMock(
        return_value= {'id': 57130362, 'src': 'm2w_800000', 'dst': 'MOCK', 'result': True}
    )

    return mock_em


@pytest.mark.asyncio
async def test_1p7k_mock_device_info(mock_1p7k) -> None:
    """
    Test for device_info method using Async Mocking
    :param mock_1p7k: Mock fixture
    :return: None
    """
    result = await mock_1p7k.Device.device_info(Device.TYPE_1P7K)
    assert result != None
    # process_1p7k_info_for_pytest(result.__dict__)
    
@pytest.mark.asyncio
async def test_1p7k_mock_device_config(mock_1p7k) -> None:
    """
    Test for device_config method using Async Mocking
    :param mock_1p7k: Mock fixture
    :return: None
    """
    result: Settings = await mock_1p7k.Device.device_config()
    assert result.type == Device.TYPE_1P7K

@pytest.mark.asyncio
async def test_1p7k_mock_send_charge_start(mock_1p7k) -> None:
    """
    Test for send_charge_start method using Async Mocking
    :param mock_1p7k: Mock fixture
    :return: None
    """
    result = await mock_1p7k.Device.send_charge_start()
    process_for_pytest(result)

@pytest.mark.asyncio
async def test_1p7k_mock_send_charge_stop(mock_1p7k) -> None:
    """
    Test for send_charge_stop method using Async Mocking
    :param mock_1p7k: Mock fixture
    :return: None
    """
    result = await mock_1p7k.Device.send_charge_stop()
    process_for_pytest(result)

@pytest.mark.asyncio
async def test_1p7k_mock_send_reset(mock_1p7k) -> None:
    """
    Test for send_reset method using Async Mocking
    :param mock_1p7k: Mock fixture
    :return: None
    """
    result = await mock_1p7k.Device.send_reset()
    process_for_pytest(result)

@pytest.mark.asyncio
async def test_1p7k_mock_set_auth(mock_1p7k) -> None:
    """
    Test for set_auth method using Async Mocking
    :param mock_1p7k: Mock fixture
    :return: None
    """
    result = await mock_1p7k.Device.set_auth()
    process_for_pytest(result)

@pytest.mark.asyncio
async def test_1p7k_mock_set_led_max_brightness(mock_1p7k) -> None:
    """
    Test for set_led_max_brightness method using Async Mocking
    :param mock_1p7k: Mock fixture
    :return: None
    """
    result = await mock_1p7k.Device.set_led_max_brightness()
    process_for_pytest(result)

@pytest.mark.asyncio
async def test_1p7k_mock_set_dynamic_current(mock_1p7k) -> None:
    """
    Test for set_dynamic_current method using Async Mocking
    :param mock_1p7k: Mock fixture
    :return: None
    """
    result = await mock_1p7k.Device.set_dynamic_current()
    process_for_pytest(result)

@pytest.mark.asyncio
async def test_1p7k_mock_set_user_current(mock_1p7k) -> None:
    """
    Test for set_user_current method using Async Mocking
    :param mock_1p7k: Mock fixture
    :return: None
    """
    result = await mock_1p7k.Device.set_user_current()
    process_for_pytest(result)

@pytest.mark.asyncio
async def test_1p7k_mock_set_charger_locked(mock_1p7k) -> None:
    """
    Test for set_charger_locked method using Async Mocking
    :param mock_1p7k: Mock fixture
    :return: None
    """
    result = await mock_1p7k.Device.set_charger_locked()
    process_for_pytest(result)


@pytest.mark.asyncio
async def test_em_mock_device_info(mock_em) -> None:
    """
    Test for device_info method using Async Mocking
    :param mock_em: Mock fixture
    :return: None
    """
    result: Settings = await mock_em.Device.device_info(Device.TYPE_EM)
    assert result != None
    
@pytest.mark.asyncio
async def test_em_mock_device_config(mock_em) -> None:
    """
    Test for device_config method using Async Mocking
    :param mock_em: Mock fixture
    :return: None
    """
    result: Settings = await mock_em.Device.device_config()
    assert result.type == Device.TYPE_EM

@pytest.mark.asyncio
async def test_em_mock_send_reset(mock_em) -> None:
    """
    Test for send_reset method using Async Mocking
    :param mock_em: Mock fixture
    :return: None
    """
    result = await mock_em.Device.send_reset()
    process_for_pytest(result)

@pytest.mark.asyncio
async def test_em_mock_set_load_balancing_mode(mock_em) -> None:
    """
    Test for set_load_balancing_mode method using Async Mocking
    :param mock_em: Mock fixture
    :return: None
    """
    result = await mock_em.Device.set_load_balancing_mode()
    process_for_pytest(result)
