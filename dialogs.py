import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

import config


class UnsetDriveDisabled(simpledialog.Dialog):

    def __init__(self, parent):
        self.cancel = False
        super().__init__(parent)

    def body(self, parent):
        self.label_frame = tk.LabelFrame(parent, text="Unset Drive Disabled")
        self.label_frame.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)

        self.explanation_text = tk.StringVar()
        self.explanation_text.set("How to deal with drive disabled?")
        explanation_label = tk.Label(self.label_frame, textvariable=self.explanation_text)
        explanation_label.grid(row=0, column=0, sticky=tk.NSEW)

        options_label_frame = tk.LabelFrame(self.label_frame, text="Options: ")
        options_label_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=10, pady=10)
        self.options_values_text = tk.StringVar()
        options = {
            "Retain disabled drive only": 1,
            "Re-enable drive and continue action": 2,
            "Finish insertion and ready probe retraction": 3
        }
        for idx, (text, value) in enumerate(options.items()):
            ttk.Radiobutton(options_label_frame, text=text,
                            variable=self.options_values_text,
                            value=value,
                            style="IndicatorOff.TRadiobutton").grid(row=idx, column=0, sticky=tk.W)

    def apply(self):
        config.options_text = self.options_values_text.get()

    def ok_pressed(self):
        self.apply()
        self.destroy()

    def cancel_pressed(self):
        self.cancel = True
        self.destroy()

    def buttonbox(self):
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(expand=True)
        self.ok_button = ttk.Button(self.button_frame, text="Submit",
                                    width=20,
                                    command=self.ok_pressed)
        self.ok_button.grid(row=0, column=0, padx=10, pady=10)
        self.cancel_button = ttk.Button(self.button_frame,
                                        text="Cancel",
                                        width=20,
                                        command=self.cancel_pressed)
        self.cancel_button.grid(row=1, column=0, padx=10, pady=10)
