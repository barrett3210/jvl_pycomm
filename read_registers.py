
import jvl_controller as jvl

import time
import numpy as np

from pycomm3 import DWORD, UINT, UDINT, BYTE, DINT, REAL, BytesDataType

if __name__ == '__main__':


    # **************
    # work with drive
    ip_address = '192.168.0.28'

    jvl_drive = jvl.JVLDrive(ip_address)

    print(jvl_drive.identity)

    print()

    print("Values in UDINT registers:")
    for number, name in zip([2, 6, 7],
                            ['Mode', 'desired acceleration', 'max torque']):
        print(number, name, jvl_drive.read_motor_register(number, data_type=UDINT))

    print()

    print("values in DINT registers: ")
    for number, name in zip([3, 5, 10],
                            ['target position', 'desired velocity', 'actual position']):
        print(number, name, jvl_drive.read_motor_register(number, data_type=DINT))

    print()

    print("module register 48 status bits: ")
    status_bits = jvl_drive.read_module_register(48, data_type=DWORD)
    for bit in [7, 9, 10, 11, 12, 13, 14, 15]:
        print(bit, int(status_bits[bit]))

    print()

    print("Module register 49, protocol type:")
    protocol_type = jvl_drive.read_module_register(49, data_type=None)
    print(protocol_type)

    print("Module register 6, setup bits")
    setup_bits = jvl_drive.read_module_register(6, data_type=DWORD)
    for bit in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        print(bit, int(setup_bits[bit]))


    # print()
    # print("Error word 35")
    # error_word = jvl_drive.read_motor_register(35, data_type=DWORD)
    # for i in range(len(error_word)):
    #     print(i, int(error_word[i]))
    #
    # print()
    # print("Control bits 36")
    # control_bits = jvl_drive.read_motor_register(36, data_type=DWORD)
    # for bit in range(len(control_bits)):
    #     print(bit, int(control_bits[bit]))

    #
    # print()
    # print("cyclic read registers:")
    # for i in [16, 17, 18, 19, 20]:
    #     print(i, jvl_drive.read_module_register(i, data_type=UDINT))
    #
    # print()
    # print("cyclic write registers:")
    # for i in [24, 25, 26, 27, 28]:
    #     print(i, jvl_drive.read_module_register(i, data_type=UDINT))
    #
    # print()

    #



