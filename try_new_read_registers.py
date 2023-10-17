import time

import jvl_controller as jvl


if __name__ == '__main__':
    ip_address = '192.168.0.28'

    jvl_drive = jvl.JVLDrive(ip_address)
    print("drive_path", jvl_drive.drive_path)
    print("Identity", jvl_drive.identity)
    print("is connected", jvl_drive.is_connected())
    time.sleep(0.5)
    print()

    position = jvl_drive.read_register('current_position')
    print(f"Current position: {position[0]} {position[1]}")
    velocity = jvl_drive.read_register('current_velocity')
    print(f"Current velocity: {velocity[0]} {velocity[1]}")
    requested_position = jvl_drive.read_register('requested_position')
    print(f"Requested position: {requested_position[0]} {requested_position[1]}")
    mode = jvl_drive.read_register('mode')
    print(f"Mode: {mode[0]}")

    print()
    for register in jvl.registers:
        value = jvl_drive.read_register(register)
        print(register, value[0], value[1])
