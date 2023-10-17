import jvl_controller as jvl

from pycomm3 import UDINT, DINT, DWORD

if __name__ == '__main__':
    # work with drive
    ip_address = '192.168.0.28'

    jvl_drive = jvl.JVLDrive(ip_address)

    print(jvl_drive.identity)

    position = jvl_drive.read_current_position()
    print(position)

    register_10 = jvl_drive.read_motor_register(10, data_type=None)
    print(register_10)

    register_10_dint = jvl_drive.read_motor_register(10, data_type=DINT)
    print(register_10_dint)

    print("Read module register 6")
    setup_bits = jvl_drive.read_module_register(6, data_type=DWORD)
    print(setup_bits)

    setup_bits[1] = True

    print(setup_bits)
    print(DWORD.encode(setup_bits))


