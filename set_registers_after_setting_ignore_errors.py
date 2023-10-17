import time

from pycomm3 import UDINT, DWORD, DINT, REAL

import jvl_controller as jvl

if __name__ == '__main__':
    ip_address = '192.168.0.28'

    jvl_drive = jvl.JVLDrive(ip_address)
    print("drive_path", jvl_drive.drive_path)
    print("Identity", jvl_drive.identity)
    print("is connected", jvl_drive.is_connected())
    time.sleep(0.5)
    print()

    print("Current settings")

    current_mode = jvl_drive.read_motor_register(2, data_type=UDINT)
    time.sleep(0.2)
    current_position = jvl_drive.read_motor_register(10, data_type=DINT)
    time.sleep(0.2)
    desired_velocity = jvl_drive.read_motor_register(5, data_type=DINT)
    print(f"Mode: {current_mode}, Position: {current_position}, "
          f"Desired_velocity: {desired_velocity}")
    print()
    time.sleep(0.5)

    module_setup_bits = jvl_drive.read_module_register(6, data_type=DWORD)
    print(f"Module register 6 setup bits")
    print(module_setup_bits)



    print("Set desired velocity")
    jvl_drive.set_motor_register(5, request_data=DINT.encode(277))
    time.sleep(0.5)

    print("Read Desired Velocity")
    print(jvl_drive.read_motor_register(5, data_type=DINT))
    time.sleep(0.5)



    print("Set operating mode to 1 (velocity):")
    jvl_drive.set_motor_register(2, request_data=DINT.encode(1))
    #
    time.sleep(2)
    print("Read operating mode")
    print(jvl_drive.read_motor_register(2, data_type=UDINT))
    print("Current Position ", jvl_drive.read_motor_register(10, data_type=DINT))
    print("Current desired velocity ", jvl_drive.read_motor_register(5, data_type=DINT))
    #
    #
    time.sleep(0.5)
    print("Set operating mode to 0 (passive):")
    jvl_drive.set_motor_register(2, request_data=DINT.encode(0))
