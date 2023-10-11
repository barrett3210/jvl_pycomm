import datetime
import numpy as np

import jvl_controller as jvl
from pycomm3 import DWORD, UINT, UDINT

import time

import tkinter as tk
from tkinter import ttk


def get_current_time():
    return np.datetime64(datetime.datetime.now()).astype(np.int64)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("JVL motor watch")
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.time_label_text = tk.StringVar()
        self.time_label_text.set("time not initialized")
        time_label = ttk.Label(self, textvariable=self.time_label_text)
        time_label.grid(row=0, column=0)

        self.operating_mode_text = tk.StringVar()
        self.operating_mode_text.set("Blah de blah")
        operating_mode_label = ttk.Label(self, textvariable=self.operating_mode_text)
        operating_mode_label.grid(row=1, column=0)

        self.position_text = tk.StringVar()
        self.position_text.set("Blah de blah")
        position_label = ttk.Label(self, textvariable=self.position_text)
        position_label.grid(row=2, column=0)

        self.velocity_text = tk.StringVar()
        self.velocity_text.set("Blah de blah")
        velocity_label = ttk.Label(self, textvariable=self.velocity_text)
        velocity_label.grid(row=3, column=0)

        self.digital_io_text = tk.StringVar()
        self.digital_io_text.set("Blah de blah")
        digital_io_label = ttk.Label(self, textvariable=self.digital_io_text)
        digital_io_label.grid(row=4, column=0)

        self.position_mode_button = ttk.Button(self, text="position mode",
                                               command=self.on_position_mode_button)
        self.position_mode_button.grid(row=5, column=0)

        self.passive_mode_button = ttk.Button(self, text="passive mode",
                                              command=self.on_passive_mode_button)
        self.passive_mode_button.grid(row=6, column=0)

        self.update_labels()

    def on_position_mode_button(self):
        jvl_drive.set_operating_mode(2)

    def on_passive_mode_button(self):
        jvl_drive.set_operating_mode(0)

    def update_labels(self, poll=True):
        now = datetime.datetime.now().time()
        self.time_label_text.set(time.strftime("%H:%M:%S"))
        operating_mode = jvl_drive.get_operating_mode()
        self.operating_mode_text.set(f"Operating mode: {operating_mode}")
        current_position = jvl_drive.read_current_position()
        self.position_text.set(f"Current position: {current_position}")
        current_velocity = jvl_drive.read_velocity()
        self.velocity_text.set(f"Current velocity: {current_velocity}")
        digital_io = jvl_drive.read_digital_io_register()
        self.digital_io_text.set(f"Digital IO: {digital_io}")

        if poll:
            self.after(20, self.update_labels)



if __name__ == '__main__':

    ip_address = '192.168.0.28'

    jvl_drive = jvl.JVLDrive(ip_address)
    print("drive_path", jvl_drive.drive_path)
    print("Identity" , jvl_drive.identity)
    print("is connected", jvl_drive.is_connected())
    time.sleep(1)
    print(jvl_drive.read_digital_io_register())

    app = Application()
    app.mainloop()




    #
    # response = jvl_drive.get_operating_mode()
    # print("original response", response)
    # time.sleep(2)
    # value = 2
    # response = jvl_drive.set_operating_mode(value)
    # print("setting mode response ", response)
    #
    # for i in range(3):
    #     response = jvl_drive.get_operating_mode()
    #     print(f"response {i}: ", response)
    #     time.sleep(2)
    #
    # value = 0
    # response = jvl_drive.set_operating_mode(value)
    # print("response to set passive mode: ", response)
    #
    # time.sleep(2)
    #
    # response = jvl_drive.get_operating_mode()
    # print("final response: ", response)

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








