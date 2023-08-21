import pytest
from lektricowifi.exceptions import DeviceConnectionError
from lektricowifi.lektricowifi import Device
from lektricowifi.models import Info, InfoForM2W, Settings, InfoForCharger

IP_OF_1P7K_DEVICE: str = "192.168.1.10"
IP_OF_EM_DEVICE: str = "192.168.1.3"

@pytest.mark.xfail
@pytest.mark.asyncio
async def test_1p7k_online_device_config():
   async with Device(IP_OF_1P7K_DEVICE) as device: 
      try:
         settings: Settings = await device.device_config()
         assert settings.type == Device.TYPE_1P7K
      except TimeoutError:
         pytest.fail(reason="TimeoutError: check if the IP is the right one", pytrace=False)
      except DeviceConnectionError:
         pytest.fail(reason="DeviceConnectionError: The device is offline", pytrace=False)

@pytest.mark.xfail
@pytest.mark.asyncio
async def test_1p7k_online_device_info():
   async with Device(IP_OF_1P7K_DEVICE) as device: 
      try:
         info: InfoForCharger = await device.device_info(Device.TYPE_1P7K)
         global current_info_for_charger
         current_info_for_charger = info
         assert info != None
      except TimeoutError:
         pytest.fail(reason="TimeoutError: check if the IP is the right one", pytrace=False)
      except DeviceConnectionError:
         pytest.fail(reason="DeviceConnectionError: The device is offline", pytrace=False)

@pytest.mark.xfail
@pytest.mark.asyncio
async def test_1p7k_online_send_charge_start():
   async with Device(IP_OF_1P7K_DEVICE) as device:
      process_for_pytest(await device.send_charge_start())

@pytest.mark.xfail
@pytest.mark.asyncio
async def test_1p7k_online_send_charge_stop():
   async with Device(IP_OF_1P7K_DEVICE) as device:
      process_for_pytest(await device.send_charge_stop())

@pytest.mark.xfail
@pytest.mark.asyncio
async def test_1p7k_online_send_reset():
   async with Device(IP_OF_1P7K_DEVICE) as device:
      process_for_pytest(await device.send_reset())

@pytest.mark.xfail
@pytest.mark.asyncio
async def test_1p7k_online_set_auth():
   async with Device(IP_OF_1P7K_DEVICE) as device:
      process_for_pytest(await device.set_auth(current_info_for_charger.require_auth))

@pytest.mark.xfail
@pytest.mark.asyncio
async def test_1p7k_online_set_led_max_brightness():
   async with Device(IP_OF_1P7K_DEVICE) as device:
      process_for_pytest(await device.set_led_max_brightness(current_info_for_charger.led_max_brightness))

@pytest.mark.xfail
@pytest.mark.asyncio
async def test_1p7k_online_set_dynamic_current():
   async with Device(IP_OF_1P7K_DEVICE) as device:
      process_for_pytest(await device.set_dynamic_current(current_info_for_charger.dynamic_current))

@pytest.mark.xfail
@pytest.mark.asyncio
async def test_1p7k_online_set_user_current():
   async with Device(IP_OF_1P7K_DEVICE) as device:
      process_for_pytest(await device.set_user_current(current_info_for_charger.user_current))

@pytest.mark.xfail
@pytest.mark.asyncio
async def test_1p7k_online_set_charger_locked():
   async with Device(IP_OF_1P7K_DEVICE) as device:
      process_for_pytest(await device.set_charger_locked(False))


###  EM tests

@pytest.mark.xfail
@pytest.mark.asyncio
async def test_em_online_device_config():
   async with Device(IP_OF_EM_DEVICE) as device: 
      try:
         settings: Settings = await device.device_config()
         assert settings.type == Device.TYPE_EM
      except TimeoutError:
         pytest.fail(reason="TimeoutError: check if the IP is the right one", pytrace=False)
      except DeviceConnectionError:
         pytest.fail(reason="DeviceConnectionError: The device is offline", pytrace=False)

@pytest.mark.xfail
@pytest.mark.asyncio
async def test_em_online_device_info():
   async with Device(IP_OF_EM_DEVICE) as device: 
      try:
         info: InfoForM2W = await device.device_info(Device.TYPE_EM)
         global current_info_for_em
         current_info_for_em = info
         assert info != None
      except TimeoutError:
         pytest.fail(reason="TimeoutError: check if the IP is the right one", pytrace=False)
      except DeviceConnectionError:
         pytest.fail(reason="DeviceConnectionError: The device is offline", pytrace=False)

@pytest.mark.xfail
@pytest.mark.asyncio
async def test_em_online_set_load_balancing_mode():
   async with Device(IP_OF_EM_DEVICE) as device:
      process_for_pytest(await device.set_load_balancing_mode(current_info_for_em.lb_mode))

@pytest.mark.xfail
@pytest.mark.asyncio
async def test_em_online_send_reset():
   async with Device(IP_OF_EM_DEVICE) as device:
      process_for_pytest(await device.send_reset())

###

def process_for_pytest(answer_of_device: dict):
   try:
      if _interpret_answer(answer_of_device):
         assert True
      else:
         pytest.fail(reason="Command not executed", pytrace=False)   
   except TimeoutError:
      pytest.fail(reason="TimeoutError: check if the IP is the right one", pytrace=False)
   except DeviceConnectionError:
      pytest.fail(reason="DeviceConnectionError: The device is offline", pytrace=False)


def _interpret_answer(answer: dict) -> bool:
   """answer ex: 
   {'id': 20520236, 'src': '1p7k_500006', 'dst': 'HASS', 'result': True}
   {'id': 20520236, 'src': '1p7k_500006', 'dst': 'HASS', 'result': False}
   {'id': 66703784, 'src': '1p7k_500006', 'dst': 'HASS', 'error': {'code': -6, 'message': 'Error uknown key.'}}"""
   if "error" in answer:
      return False
   elif "result" in answer:
      return answer["result"] == True
   else:
      return False

   