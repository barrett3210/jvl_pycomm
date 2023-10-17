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

    print("Register 35")
    register_35 = jvl_drive.read_motor_register(35, data_type=DWORD)
    print(register_35)

    v_soll = jvl_drive.read_motor_register(5, data_type=DINT)
    print(f"Current v_soll {v_soll}")

    v1 = jvl_drive.read_motor_register(65, data_type=DINT)
    print(f"Current v1 {v1}")

    print("Issue module command 16777452")
    jvl_drive.set_module_register(15, request_data=DINT.encode(16777452))
    print(DINT.encode(16777452))

    v_soll = jvl_drive.read_motor_register(5, data_type=DINT)
    print(f"Current v_soll {v_soll}")

    p_soll = jvl_drive.read_motor_register(3, data_type=DINT)
    p_ist = jvl_drive.read_motor_register(10, data_type=DINT)
    p7 = jvl_drive.read_motor_register(61, data_type=DINT)
    print(f"Current p_soll {p_soll}, current p_ist {p_ist}, current p7 {p7}")

    print("Issue module command 16777457")
    jvl_drive.set_module_register(15, request_data=DINT.encode(16777457))
    p_soll = jvl_drive.read_motor_register(3, data_type=DINT)
    print(f"New p_soll {p_soll}")
