from dataclasses import dataclass
import time

from io import BytesIO
import bitstring

from typing import Any, Type, Dict, Tuple, Union

from pycomm3 import CIPDriver
from pycomm3 import Services
from pycomm3 import Struct

from pycomm3 import UDINT
from pycomm3 import DWORD
from pycomm3 import SHORT_STRING
from pycomm3 import STRING
from pycomm3 import DINT
from pycomm3 import BYTE
from pycomm3 import UINT

from pycomm3.cip import n_bytes

import config


# from config import read_assembly, requested_items, in_position, Convert
# from config import move_down_distance


def discover_drive_addresses():
    drives = CIPDriver.discover()
    ip_addresses = [drive['ip_address'] for drive in drives]
    return ip_addresses


class ReadAssembly(Struct(
    DINT('operating mode'),
    DINT('position'),
    DINT('velocity'),
    DWORD('register 35'),
    DWORD('digital inputs'),
)):
    @classmethod
    def _decode(cls, stream: BytesIO):
        values = super(ReadAssembly, cls)._decode(stream)
        return values

    @classmethod
    def _encode(cls, values: Dict[str, Any]):
        values = values.copy()
        return super(ReadAssembly, cls._encode(values))


class WriteAssembly(Struct(
    DINT('operating mode'),
    DINT('module command'),
    DINT('write word 3'),
    DINT('write word 4'),
    DINT('write word 5')
)):
    ...


def get_current_stored_position_cm():
    current_position_cm = config.read_assembly['position'] * config.Convert.COUNT2CM.value
    return current_position_cm


class JVLDrive:
    def __init__(self, drive_path):
        self.drive_path = drive_path
        self.connected = self.is_connected()
        self.identity = self.identify_drive()
        self.status = self.identity['status']
        self.set_operating_mode(0)
        self.set_startup_registers()

    def is_connected(self):
        with CIPDriver(self.drive_path) as drive:
            return drive.connected

    def identify_drive(self):
        with CIPDriver(self.drive_path) as drive:
            return drive.list_identity(self.drive_path)

    def set_startup_registers(self):
        for register in config.startup_register_values:
            self.set_motor_register(
                register,
                request_data=DINT.encode(config.startup_register_values[register]))

    def read_motor_register(self, register, data_type=None):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x64',
                instance=register,
                attribute=b'\x01',
                data_type=data_type,
            )
        return param.value

    def read_module_register(self, register, data_type=None):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x65',
                instance=register,
                attribute=b'\x01',
                data_type=data_type,
            )
        return param.value

    def set_motor_register(self, register,
                           data_type=None,
                           request_data=None):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.set_attribute_single,
                class_code=b'\x64',
                instance=register,
                attribute=b'\x01',
                data_type=data_type,
                request_data=request_data
            )
        return param

    def set_module_register(self, register,
                            data_type=None,
                            request_data=None):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.set_attribute_single,
                class_code=b'\x65',
                instance=register,
                attribute=b'\x01',
                data_type=data_type,
                request_data=request_data
            )
        return param

    def get_operating_mode(self):
        mode = self.read_assembly_object_portion('operating mode')

    def set_operating_mode(self, value):
        write_assembly = [value, 0, 0, 0, 0]
        self.issue_cyclic_command(WriteAssembly.encode(write_assembly))
        if value == 0:
            config.enable_drive = False
        else:
            config.enable_drive = True
            config.requested_mode = value
        # print(f"value {value}, config.requested_mode {config.requested_mode}")

    def read_assembly_object_portion(self, portion):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x04',
                instance=b'\x65',
                attribute=b'\x03',
                data_type=ReadAssembly,
                name='read assembly'
            )
        return param.value[portion]

    def read_assembly_object(self):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x04',
                instance=b'\x65',
                attribute=b'\x03',
                data_type=ReadAssembly,
            )
        return param.value

    def issue_cyclic_command(self, command):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.set_attribute_single,
                class_code=b'\x04',
                instance=b'\x64',
                attribute=b'\x03',
                request_data=command,
            )

    def read_current_position(self):
        position = self.read_assembly_object_portion('position')
        return position

    def read_velocity(self):
        velocity = self.read_assembly_object_portion('velocity')
        return velocity

    def read_digital_inputs(self):
        inputs = self.read_assembly_object_portion('digital inputs')
        return inputs[:3]

    def read_error_register(self):
        register_35 = self.read_assembly_object_portion('register 35')
        return register_35

    def read_module_status_bits(self):
        module_status = self.read_module_register(48, data_type=DWORD)
        return module_status

    def read_control_bits(self):
        control_bits = self.read_motor_register(36, data_type=DWORD)

    def read_requested_items(self):
        requested_position = self.read_motor_register(3, data_type=DINT)
        requested_velocity = self.read_motor_register(5, data_type=DINT)
        requested_torque = self.read_motor_register(7, data_type=DINT)
        return (requested_position, requested_velocity, requested_torque)

    def set_requested_position(self, requested_position_cm):
        requested_position_counts = int(requested_position_cm * config.Convert.CM2COUNT.value)
        self.set_motor_register(3, request_data=DINT.encode(requested_position_counts))

    def move_down(self, move_down_cm):
        print("jvl drive move down")
        current_position_cm = get_current_stored_position_cm()
        print("Current position ", current_position_cm)
        requested_position_cm = current_position_cm + move_down_cm
        print("Requested position ", requested_position_cm)
        self.set_requested_position(requested_position_cm)
        time.sleep(0.005)
        self.set_operating_mode(2)
        print("finished jvl drive move down")

    def retract_probe(self, position_cm):
        print("jvl drive retract probe")
        print(f"Request to move to position {position_cm} cm")
        self.set_requested_position(position_cm)
        time.sleep(0.005)
        self.set_operating_mode(2)
        print("finished jvl drive retract probe")

    def move_to_insertion_stop(self, stop):
        # print("jvl drive move to stop")
        requested_position_cm = stop
        print("Requested position ", requested_position_cm)
        self.set_requested_position(requested_position_cm)
        time.sleep(0.005)
        self.set_operating_mode(2)
        # print("finished jvl drive move to next stop")
