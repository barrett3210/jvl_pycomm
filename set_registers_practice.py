import time

from pycomm3 import UDINT, DWORD, DINT, REAL

import jvl_controller as jvl

if __name__ == '__main__':
    ip_address = '192.168.0.28'

    jvl_drive = jvl.JVLDrive(ip_address)
    print("drive_path", jvl_drive.drive_path)
    print("Identity", jvl_drive.identity)
    print("is connected", jvl_drive.is_connected())
    time.sleep(1)


    print()
    print("Read Operating mode")
    print(jvl_drive.read_motor_register(2, data_type=UDINT))
    time.sleep(0.5)
    print("Read Current Position")
    print(jvl_drive.read_motor_register(10, data_type=DINT))
    print("Read Desired Velocity")
    print(jvl_drive.read_motor_register(5, data_type=DINT))
    print("Read P7")
    print(jvl_drive.read_motor_register(63, data_type=DINT))
    time.sleep(0.5)

    jvl_drive.set_motor_register(63, request_data=DINT.encode(100000))
    time.sleep(0.5)

    print(jvl_drive.read_motor_register(63, data_type=DINT))
    time.sleep(0.5)

    print("Set desired velocity")
    print(jvl_drive.set_motor_register(5, request_data=DINT.encode(277)))
    time.sleep(0.5)

    print("Read Desired Velocity")
    print(jvl_drive.read_motor_register(5, data_type=DINT))
    time.sleep(0.5)

    print("Set velocity mode")



    # print("Set Desired Velocity")
    # jvl_drive.set_motor_register(5, request_data=REAL.encode(277))
    # print("Read Desired Velocity")
    # print(jvl_drive.read_motor_register(5, data_type=REAL))

    time.sleep(0.5)
    print("Set operating mode to 1 (velocity):")
    jvl_drive.set_motor_register(2, request_data=DINT.encode(1))
    #
    time.sleep(1)
    print("Read operating mode")
    print(jvl_drive.read_motor_register(2, data_type=UDINT))
    print("Current Position ", jvl_drive.read_motor_register(10, data_type=DINT))
    # print("Current desired velocity ", jvl_drive.read_motor_register(5, data_type=DINT))
    #
    #
    time.sleep(0.5)
    print("Set operating mode to 0 (passive):")
    jvl_drive.set_motor_register(2, request_data=DINT.encode(0))
