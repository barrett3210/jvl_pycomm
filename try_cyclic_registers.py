import time

from io import BytesIO
import bitstring

from typing import Any, Type, Dict, Tuple, Union

from pycomm3 import UDINT, DWORD, DINT, REAL
from pycomm3 import Struct

import jvl_controller
import jvl_controller as jvl


def calculate_position_cm(position_counts):
    position_cm = (position_counts * 0.169418) / 8192
    return position_cm





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

    print("Cyclic register 35")
    cyclic_response = jvl_drive.read_assembly_object_portion('register 35')
    print(cyclic_response)

    mode = jvl_drive.read_motor_register(2, data_type=DINT)
    mode_cyclic = jvl_drive.read_assembly_object_portion('operating mode')
    print(f"Mode {mode}, mode from cyclic {mode_cyclic}")

    position = jvl_drive.read_motor_register(10, data_type=DINT)
    position_cyclic = jvl_drive.read_assembly_object_portion('position')
    print(f"Position {position}, position cyclic {position_cyclic}")
    position_cm = calculate_position_cm(position_cyclic)
    print(f"Position in cm {position_cm} cm")

    velocity = jvl_drive.read_motor_register(11, data_type=DINT)
    velocity_cyclic = jvl_drive.read_assembly_object_portion('velocity')
    print(f"Velocity {velocity}, velocity cyclic {velocity_cyclic}")

    digital_inputs = jvl_drive.read_module_register(47, data_type=DWORD)
    digital_inputs_cyclic = jvl_drive.read_assembly_object_portion('digital inputs')
    print("regular digital inputs")
    print(digital_inputs)
    print("cyclic digital inputs")
    print(digital_inputs_cyclic)

    time.sleep(1)
    print("Set requested velocity")
    jvl_drive.set_motor_register(5, request_data=DINT.encode(277))
    print("Issue cyclic change to operating mode")
    command = [1, 0, 0, 0, 0]
    jvl_drive.issue_cyclic_command(jvl.WriteAssembly.encode(command))
    print(f"Current mode: {jvl_drive.read_assembly_object_portion('operating mode')}")
    time.sleep(2)
    print("Set mode to 0")
    command = [0, 0, 0, 0, 0]
    jvl_drive.issue_cyclic_command(jvl.WriteAssembly.encode(command))
    time.sleep(1)
    print("set mode to 1")
    write_trial = [1, 0, 0, 0, 0]
    jvl_drive.issue_cyclic_command(jvl.WriteAssembly.encode(write_trial))
    print(f"Current mode: {jvl_drive.read_assembly_object_portion('operating mode')}")

    time.sleep(1)
    print("set mode to zero")
    write_trial = [0, 0, 0, 0, 0]
    jvl_drive.issue_cyclic_command(jvl.WriteAssembly.encode(write_trial))
    time.sleep(1)
    print(f"Current mode: {jvl_drive.read_assembly_object_portion('operating mode')}")

    current_position = calculate_position_cm(jvl_drive.read_assembly_object_portion('position'))
    print(f"Current position is {current_position} cm")

    read_assembly = jvl_drive.read_assembly_object()
    print("read_assembly")
    print(read_assembly)
    for key in read_assembly:
        print(key, read_assembly[key])




    print(jvl_controller.WriteAssembly.encode(write_trial))







    # looking at module command 15


    #
    # v_soll = jvl_drive.read_motor_register(5, data_type=DINT)
    # print(f"Current v_soll {v_soll}")
    #
    # v1 = jvl_drive.read_motor_register(65, data_type=DINT)
    # print(f"Current v1 {v1}")
    #
    # print("Issue module command 16777452")
    # jvl_drive.set_module_register(15, request_data=DINT.encode(16777452))
    # print(DINT.encode(16777452))
    #
    # v_soll = jvl_drive.read_motor_register(5, data_type=DINT)
    # print(f"Current v_soll {v_soll}")
    #
    # p_soll = jvl_drive.read_motor_register(3, data_type=DINT)
    # p_ist = jvl_drive.read_motor_register(10, data_type=DINT)
    # p7 = jvl_drive.read_motor_register(61, data_type=DINT)
    # print(f"Current p_soll {p_soll}, current p_ist {p_ist}, current p7 {p7}")
    #
    # print("Issue module command 16777457")
    # jvl_drive.set_module_register(15, request_data=DINT.encode(16777457))
    # p_soll = jvl_drive.read_motor_register(3, data_type=DINT)
    # print(f"New p_soll {p_soll}")
