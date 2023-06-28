# LektricoWifi 

This is a package for communicating with *[Lektrico](https://lektri.co/)*'s chargers (1P7K, 3P22K) and devices (EM, 3EM) when they are in your wifi network.

You have to know the IP of your device.

## What is this package offering:
1. Identify your device by IP

  type, serial_number, board_revision
   
2. Ready the device's parameters

  currents, voltages, powers, errors, ...
  
  see the output in the examples below the
    
3. Command the device

commands for charger:

- start charging: send_charge_start
- stop charging: send_charge_stop
- reset the device: send_reset
- enable/disable authorisation: set_auth
- set leds brightness: set_led_max_brightness
- set the dynamic current: set_dynamic_current
- set the user current: set_user_current
- lock/unlock the device: set_charger_locked

commands for em:

- set the load balancing mode (OFF, POWER, HYBRID, GREEN): set_load_balancing_mode
- reset the device: send_reset

## How to use it:
1. Find the IP of your Lektrico device in your local wifi network
2. Install it in your python project's environment
   
   pip install lektricowifi==0.0.25
   
3. Install the required library

   pip install aiohttp

4. Python example for charger: (python 3.11.0)

        import asyncio
        from lektricowifi import Device
        from lektricowifi.models import Info, Settings
        
        async def main():
            """Example of communicating with a Lektrico charger."""
            
            # use your device's IP!
            async with Device("192.168.100.11") as device:
            
                # identify your device's type
                settings: Settings = await device.device_config()
                print(settings)
                """output:  Settings(type='1p7k', serial_number=500006, board_revision='E')"""
                print(settings.type)
                """output:  1p7k"""
                
                # read your device's parameters
                info: Info = await device.device_info(Device.TYPE_1P7K)
                print(info)
                """output:  InfoForCharger(current_l1=0.0, current_l2=0.0, current_l3=0.0, 
                voltage_l1=0.0, voltage_l2=0.0, voltage_l3=0.0, fw_version='1.45_beta', 
                charger_state='Available', session_energy=0.0, charging_time=0, 
                instant_power=0.0, temperature=39.8, dynamic_current=32, require_auth=False, 
                install_current=6, led_max_brightness=100, total_charged_energy=18.0, 
                has_active_errors=False, state_e_activated=False, overtemp=False, 
                critical_temp=False, overcurrent=False, meter_fault=False, 
                undervoltage_error=False, overvoltage_error=False, rcd_error=False, 
                cp_diode_failure=False, contactor_failure=False, user_current=32, 
                current_limit_reason='Installation current')"""
        
                # command the charger to start charging
                answer: bool = await device.send_charge_start()
                print(answer)
                """output:  {'id': 57130362, 'src': '1p7k_500006', 'dst': 'HASS', 'result': True}"""
        
         
        if __name__ == "__main__":
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main())
   
5. Python example for em device: (python 3.11.0)

        import asyncio
        from lektricowifi import Device, LBMode
        from lektricowifi.models import Info, Settings

        async def main():
            """Example of communicating with a Lektrico device."""
            
            # use your device's IP!
            async with Device("192.168.100.201") as device:  
               
                # identify your device's type
                settings: Settings = await device.device_config()
                print(settings) 
                """output:  Settings(type='em', serial_number=810172, board_revision='A')"""
                print(settings.type)
                """output:  em"""
        
                # read your device's parameters
                info: Info = await device.device_info(Device.TYPE_EM)
                print(info)
                """output:  InfoForM2W(current_l1=0.0, current_l2=0.0, current_l3=0.0, 
                voltage_l1=230.968, voltage_l2=230.968, voltage_l3=0.1,fw_version='1.15', 
                power_l1=0.0, power_l2=0.0, power_l3=0.0, breaker_curent=32, power_factor_l1=0.0, 
                power_factor_l2=0.0, power_factor_l3=0.0, lb_mode=0)"""
        
                # command the em to change the load balancing mode
                answer: bool = await device.set_load_balancing_mode(LBMode.GREEN.value)
                print(answer)
                """output:  {'id': 32647575, 'src': 'm2w_810172', 'dst': 'HASS', 'result': True}"""
        
         
        if __name__ == "__main__":
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main())
