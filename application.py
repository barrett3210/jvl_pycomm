import jvl_controller as jvl
from pycomm3 import DWORD, UINT, UDINT

import time



if __name__ == '__main__':

    ip_address = '192.168.0.28'

    jvl_drive = jvl.JVLDrive(ip_address)
    print("drive_path", jvl_drive.drive_path)
    print("Identity" , jvl_drive.identity)
    time.sleep(2)

    response = jvl_drive.get_operating_mode()
    print("original response", response)
    time.sleep(2)
    value = 2
    response = jvl_drive.set_operating_mode(value)
    print("setting mode response ", response)

    for i in range(3):
        response = jvl_drive.get_operating_mode()
        print(f"response {i}: ", response)
        time.sleep(2)

    value = 0
    response = jvl_drive.set_operating_mode(value)
    print("response to set passive mode: ", response)

    time.sleep(2)

    response = jvl_drive.get_operating_mode()
    print("final response: ", response)

    # from pycomm3 import CIPDriver
    # from pycomm3 import Services
    #
    # driver = CIPDriver(ip_address)
    # driver.open()
    #
    # time.sleep(2)
    #
    # response = driver.generic_message(
    #     service=Services.set_attribute_single,
    #     class_code=b'\x64',
    #     instance=b'\x02',
    #     attribute=b'\x01',
    #     data_type=None,
    #     request_data=b'\x02\x00\x00\x00',
    # )
    # print(f"response to set to position mode: ", response)
    #
    # for i in range(3):
    #
    #     response = driver.generic_message(
    #         service=Services.get_attribute_single,
    #         class_code=b'\x64',
    #         instance=b'\x02',
    #         attribute=b'\x01',
    #         data_type=None,
    #     )
    #     print(f"response {i}: ", response)
    #
    #     time.sleep(3)
    #
    # response = driver.generic_message(
    #     service=Services.set_attribute_single,
    #     class_code=b'\x64',
    #     instance=b'\x02',
    #     attribute=b'\x01',
    #     data_type=None,
    #     request_data=b'\x00\x00\x00\x00',
    # )
    # print(f"response to set passive: ", response)
    #
    # time.sleep(3)
    #
    # response = driver.generic_message(
    #     service=Services.get_attribute_single,
    #     class_code=b'\x64',
    #     instance=b'\x02',
    #     attribute=b'\x01',
    #     data_type=None,
    # )
    # print(f"response: ", response)
    #
    # time.sleep(3)
    #
    #
    #
    # driver.close()

    # value = 2
    # response1 = jvl_drive.set_operating_mode(value)
    # print(response1)
    # print(UDINT.encode(value))
    #
    # time.sleep(2)
    #
    # value = 500
    #
    # response = jvl_drive.set_pos_reg_7(value)
    # print(UDINT.encode(value))
    # print(response)



    # print("velocity ", jvl_drive.read_velocity())
    # print("position ", jvl_drive.read_current_position())








