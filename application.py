import datetime
import time

import numpy as np


from pycomm3 import DINT

import tkinter as tk
from tkinter import ttk
from tkinter import font

import config

import jvl_controller as jvl


# from config import read_assembly, requested_items, in_position, Convert


def get_current_time():
    return np.datetime64(datetime.datetime.now()).astype(np.int64)


def on_position_mode_button():
    jvl_drive.set_operating_mode(2)


def on_passive_mode_button():
    jvl_drive.set_operating_mode(0)


def on_homing_button():
    config.homed = False
    config.my_in_position = False
    jvl_drive.set_operating_mode(12)
    app.after_idle(wait_for_mode_0)
    print("end of on_homing_button")


def on_velocity_mode_button():
    jvl_drive.set_operating_mode(0)
    app.after(100)
    jvl_drive.set_operating_mode(1)


def on_move_down_button():
    print("Pushed moved down button!")
    config.my_in_position = False
    jvl_drive.move_down()
    app.after_idle(wait_for_in_position)
    print("end of on_move_down_button")


def on_retract_probe_button():
    print("retract probe")
    config.my_in_position = False
    jvl_drive.retract_probe()
    app.after_idle(wait_for_in_position)
    print("end of on_retract_probe_button")


def wait_for_in_position():
    config.read_assembly = jvl_drive.read_assembly_object()
    config.in_position = config.read_assembly['register 35'][4]
    if config.in_position:
        print("In position?????")
        jvl_drive.set_operating_mode(0)
        config.my_in_position = True
        return
    app.after(200, wait_for_in_position)


def wait_for_mode_0():
    app.after(20)
    config.read_assembly = jvl_drive.read_assembly_object()
    in_mode_0 = config.read_assembly['operating mode']
    if in_mode_0 == 0:
        print("In mode zero!!")
        config.homed = True
        config.my_in_position = True
        return
    app.after(200, wait_for_mode_0)


class LabelsFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, **kwargs)

        self.time_label_text = tk.StringVar()
        self.time_label_text.set("time not initialized")
        time_label = ttk.Label(self, textvariable=self.time_label_text, style='My.TLabel')
        time_label.grid(row=0, column=0)
        print(f"time label style: {time_label['style']}")

        self.operating_mode_text = tk.StringVar()
        self.operating_mode_text.set("Blah de blah")
        operating_mode_intro = ttk.Label(self, text="Operating mode")
        operating_mode_intro.grid(row=1, column=0, sticky=tk.E, padx=10)
        operating_mode_label = ttk.Label(self, textvariable=self.operating_mode_text)
        operating_mode_label.grid(row=1, column=1, sticky=tk.EW, padx=10)

        self.position_text = tk.StringVar()
        self.position_text.set("Blah de blah")
        position_intro = ttk.Label(self, text="Current position")
        position_intro.grid(row=2, column=0, sticky=tk.E, padx=10)
        position_label = ttk.Label(self, textvariable=self.position_text)
        position_label.grid(row=2, column=1, sticky=tk.EW, padx=10)

        self.velocity_text = tk.StringVar()
        self.velocity_text.set("Blah de blah")
        velocity_intro = ttk.Label(self, text="Current velocity")
        velocity_intro.grid(row=3, column=0, sticky=tk.E, padx=10)
        velocity_label = ttk.Label(self, textvariable=self.velocity_text)
        velocity_label.grid(row=3, column=1, sticky=tk.EW, padx=10)

        self.digital_io_text = tk.StringVar()
        self.digital_io_text.set("Blah de blah")
        digital_io_intro = ttk.Label(self, text=f"\nInput 1\nInput 2\nInput 3\n")
        digital_io_intro.grid(row=5, column=0, sticky=tk.E, padx=10)
        digital_io_label = ttk.Label(self, textvariable=self.digital_io_text)
        digital_io_label.grid(row=5, column=1, sticky=tk.EW, padx=10)

        self.error_register_text = tk.StringVar()
        self.error_register_text.set("Blah")
        error_register_intro = ttk.Label(self, text=f"In position\nAny error\n")
        error_register_intro.grid(row=6, column=0, sticky=tk.E, padx=10)
        error_register_label = ttk.Label(self,
                                         textvariable=self.error_register_text)
        error_register_label.grid(row=6, column=1, sticky=tk.EW, padx=10)

        self.requested_items_text = tk.StringVar()
        self.requested_items_text.set("Blah")
        requested_items_intro = ttk.Label(self, text=f"\nRequested position\nRequested velocity"
                                                     f"\nRequested torque\n")
        requested_items_intro.grid(row=7, column=0, sticky=tk.E, padx=10)
        requested_items_label = ttk.Label(self, textvariable=self.requested_items_text)
        requested_items_label.grid(row=7, column=1, sticky=tk.EW, padx=10)

        self.homed_text = tk.StringVar()
        self.homed_text.set("Blah")
        homed_label_intro = ttk.Label(self, text="Homed")
        homed_label_intro.grid(row=8, column=0, sticky=tk.E, padx=10)
        homed_label = ttk.Label(self, textvariable=self.homed_text)
        homed_label.grid(row=8, column=1, sticky=tk.EW, padx=10)

        self.my_position_text = tk.StringVar()
        self.my_position_text.set("Blah")
        my_position_intro = ttk.Label(self, text="Reached Position")
        my_position_intro.grid(row=9, column=0, sticky=tk.E, padx=10)
        my_position_label = ttk.Label(self, textvariable=self.my_position_text)
        my_position_label.grid(row=9, column=1, sticky=tk.EW, padx=10)


class ActionsFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ***** Buttons *****

        self.passive_mode_button = ttk.Button(self, text="passive mode",
                                              command=on_passive_mode_button)
        self.passive_mode_button.grid(row=8, column=0)

        self.velocity_mode_button = ttk.Button(self, text="velocity mode",
                                               command=on_velocity_mode_button)
        self.velocity_mode_button.grid(row=9, column=0)

        self.position_mode_button = ttk.Button(self, text="position mode",
                                               command=on_position_mode_button)
        self.position_mode_button.grid(row=10, column=0)

        self.homing_button = ttk.Button(self,
                                        text="Homing",
                                        command=on_homing_button)
        self.homing_button.grid(row=13, column=0)

        # ***** Buttons end *****

        # ***** Entries *****
        self.position_request_intro = ttk.Label(self, text="Request position (cm): ")
        self.position_request_intro.grid(row=17, column=0)
        self.position_request_text = tk.StringVar()
        self.position_request = ttk.Entry(self, textvariable=self.position_request_text, width=5)
        self.position_request.grid(row=17, column=1, sticky=tk.EW, padx=10)
        self.position_request_button = ttk.Button(self,
                                                  text="Enter",
                                                  width=6,
                                                  command=self.on_position_request_button)
        self.position_request_button.grid(row=17, column=2)

        self.velocity_request_intro = ttk.Label(self, text="Request velocity (cm/s): ")
        self.velocity_request_intro.grid(row=18, column=0)
        self.velocity_request_text = tk.StringVar()
        self.velocity_request = ttk.Entry(self, textvariable=self.velocity_request_text, width=5)
        self.velocity_request.grid(row=18, column=1, sticky=tk.EW, padx=10)
        self.velocity_request_button = ttk.Button(self,
                                                  text="Enter",
                                                  width=6,
                                                  command=self.on_velocity_request_button)
        self.velocity_request_button.grid(row=18, column=2)

        # ***** Entries end *******

        # ***** Special buttons *****

        self.move_down_button = ttk.Button(self, text="Move down", command=on_move_down_button)
        self.move_down_button.grid(row=30, column=0)

        self.retract_probe_button = ttk.Button(self, text="Retract probe",
                                               command=on_retract_probe_button)
        self.retract_probe_button.grid(row=31, column=0)

    def on_position_request_button(self):
        position_request = float(self.position_request_text.get())
        print(position_request)
        jvl_drive.set_motor_register(
            3,
            request_data=DINT.encode(int(position_request * config.Convert.CM2COUNT.value)))

    def on_velocity_request_button(self):
        velocity_request = float(self.velocity_request_text.get())
        print(velocity_request)
        jvl_drive.set_motor_register(
            5,
            request_data=DINT.encode(
                int(velocity_request * config.Convert.CMSEC2VELOCITY.value)))


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("JVL motor watch")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure(
            'IndicatorOff.TRadiobutton',
            indicatorrelief=tk.FLAT,
            indicatormargin=1,
            indicatordiameter=10,
            relief=tk.RAISED,
            focusthickness=2,
            highlightthickness=2,
            padding=5,
            background='snow'
        )
        self.style.configure('My.TLabel', background='snow2')
        self.style.map('IndicatorOff.TRadiobutton',
                       background=[('selected', 'dark sea green'), ('active', 'DarkSeaGreen3')])
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(size=11)
        self.menu_font = font.nametofont("TkMenuFont")
        self.menu_font.configure(size=11, weight=font.BOLD)

        self.labels_frame = LabelsFrame(self, padding="20 20 20 20")
        self.labels_frame.grid(row=0, column=1, sticky=tk.NSEW)

        self.actions_frame = ActionsFrame(self, padding="20 20 20 20")
        self.actions_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.tk_in_position = tk.BooleanVar()

        # ************
        # update labels
        # ************
        self.update_labels()

    def update_labels(self, poll=True):
        now = datetime.datetime.now().time()
        self.labels_frame.time_label_text.set(time.strftime("%H:%M:%S"))

        config.read_assembly = jvl_drive.read_assembly_object()
        # the enable switch option
        # need a way to reset and return to action or leave it.
        # if not read_assembly['digital inputs'][0]:
        #     jvl_drive.set_operating_mode(0)
        config.in_position = config.read_assembly['register 35'][4]
        self.tk_in_position.set(config.in_position)
        self.labels_frame.operating_mode_text.set(f"{config.read_assembly['operating mode']}")
        self.labels_frame.position_text.set(
            f"{config.read_assembly['position'] * config.Convert.COUNT2CM.value:0.1f} cm")

        self.labels_frame.velocity_text.set(
            f"{config.read_assembly['velocity'] * config.Convert.VELOCITY2CMSEC.value:0.2f} cm/s")
        self.labels_frame.digital_io_text.set(f"\n{int(config.read_assembly['digital inputs'][0])}\n"
                                              f"{int(config.read_assembly['digital inputs'][1])}\n"
                                              f"{int(config.read_assembly['digital inputs'][2])}\n")
        self.labels_frame.error_register_text.set(f"{int(config.read_assembly['register 35'][4])}\n"
                                                  f"{int(config.read_assembly['register 35'][24])}\n")
        config.requested_items = jvl_drive.read_requested_items()
        self.labels_frame.requested_items_text.set(
            f"\n{config.requested_items[0] * config.Convert.COUNT2CM.value:0.1f} cm\n"
            f"{config.requested_items[1] * config.Convert.VELOCITY2CMSEC.value:0.2f} cm/s\n"
            f"{config.requested_items[2] * config.Convert.TORQUE2PCT.value:0.1f} %\n")
        self.labels_frame.homed_text.set(
            config.homed
        )
        self.labels_frame.my_position_text.set(
            config.my_in_position
        )
        if poll:
            self.after(10, self.update_labels)


if __name__ == '__main__':
    ip_address = '192.168.0.28'

    jvl_drive = jvl.JVLDrive(ip_address)
    print("drive_path", jvl_drive.drive_path)
    print("Identity", jvl_drive.identity)
    print("is connected", jvl_drive.is_connected())
    time.sleep(1)

    app = Application()
    app.mainloop()