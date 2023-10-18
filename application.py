import datetime
import time

import numpy as np

import jvl_controller as jvl
from pycomm3 import DWORD, UINT, UDINT, DINT

import tkinter as tk
from tkinter import ttk


# Multiply the first by value to get the second
CONVERSIONS = {
    'counts to cm': 0.0000206809,
    'cm to counts': 48353.795,
}


def get_current_time():
    return np.datetime64(datetime.datetime.now()).astype(np.int64)


def on_position_mode_button():
    jvl_drive.set_operating_mode(2)


def on_passive_mode_button():
    jvl_drive.set_operating_mode(0)


def on_homing_button():
    jvl_drive.set_operating_mode(12)


def on_velocity_mode_button():
    jvl_drive.set_operating_mode(0)
    app.after(100)
    jvl_drive.set_operating_mode(1)


def on_change_velocity_direction():
    current_desired_velocity = jvl_drive.read_motor_register(5,
                                                             data_type=DINT)
    print(f"Current desired velocity:  {current_desired_velocity}")
    new_desired_velocity = DINT.encode(-1 * current_desired_velocity)
    print(f"New desired velocity: {new_desired_velocity}")
    jvl_drive.set_motor_register(5, request_data=new_desired_velocity)
    print("set motor register 5")


def on_print_error_bits_button():
    read_assembly = jvl_drive.read_assembly_object()
    print("Error register bits: ")
    print(read_assembly['register 35'])
    print()


def on_move_to_position_try_button():
    print("Move to position")
    print("need to update this command")
    # position = 900
    # jvl_drive.set_requested_position_register(position)


def on_command_register_button():
    print("activate command register")
    print("need to update this command")


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

        self.error_register_text = tk.StringVar()
        self.error_register_text.set("Blah")
        error_register_label = ttk.Label(self,
                                         textvariable=self.error_register_text)
        error_register_label.grid(row=5, column=0)

        # *************
        # Buttons
        # Currently begin row 9
        # *************

        self.velocity_mode_button = ttk.Button(self, text="velocity mode",
                                               command=on_velocity_mode_button)
        self.velocity_mode_button.grid(row=9, column=0)

        self.position_mode_button = ttk.Button(self, text="position mode",
                                               command=on_position_mode_button)
        self.position_mode_button.grid(row=10, column=0)

        self.passive_mode_button = ttk.Button(self, text="passive mode",
                                              command=on_passive_mode_button)
        self.passive_mode_button.grid(row=11, column=0)

        self.print_error_bits_button = ttk.Button(self,
                                                  text="Print error bits",
                                                  command=on_print_error_bits_button)
        self.print_error_bits_button.grid(row=12, column=0)

        self.homing_button = ttk.Button(self,
                                        text="Homing",
                                        command=on_homing_button)
        self.homing_button.grid(row=13, column=0)

        self.move_to_position_try_button = ttk.Button(self,
                                                      text="Move",
                                                      command=on_move_to_position_try_button)
        self.move_to_position_try_button.grid(row=14, column=0)

        self.command_register_button = ttk.Button(self,
                                                  text="Command Register",
                                                  command=on_command_register_button)
        self.command_register_button.grid(row=15, column=0)

        self.change_velocity_direction_button = ttk.Button(self,
                                                           text="Change direction",
                                                           command=on_change_velocity_direction)
        self.change_velocity_direction_button.grid(row=16, column=0)

        # ************
        # update labels
        # ************
        self.update_labels()

    def update_labels(self, poll=True):
        now = datetime.datetime.now().time()
        self.time_label_text.set(time.strftime("%H:%M:%S"))

        read_assembly = jvl_drive.read_assembly_object()
        self.operating_mode_text.set(f"Operating mode: {read_assembly['operating mode']}")
        self.position_text.set(f"Current position: {read_assembly['position'] * CONVERSIONS['counts to cm']:0.2f} cm")
        self.velocity_text.set(f"Current velocity: {read_assembly['velocity']}")
        self.digital_io_text.set(f"Input 1: {read_assembly['digital inputs'][0]}\n"
                                 f"Input 2: {read_assembly['digital inputs'][1]}\n"
                                 f"Input 3: {read_assembly['digital inputs'][2]}\n")
        self.error_register_text.set(f"In position: {read_assembly['register 35'][4]}\n"
                                     f"Accelerating: {read_assembly['register 35'][5]}\n"
                                     f"Decelerating: {read_assembly['register 35'][6]}\n"
                                     f"Position Limit: {read_assembly['register 35'][7]}\n"
                                     f"Any error: {read_assembly['register 35'][24]}\n")
        if poll:
            self.after(100, self.update_labels)

if __name__ == '__main__':

    ip_address = '192.168.0.28'

    jvl_drive = jvl.JVLDrive(ip_address)
    print("drive_path", jvl_drive.drive_path)
    print("Identity", jvl_drive.identity)
    print("is connected", jvl_drive.is_connected())
    time.sleep(1)

    app = Application()
    app.mainloop()









