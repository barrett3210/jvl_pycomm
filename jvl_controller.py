from dataclasses import dataclass


from pycomm3 import CIPDriver
from pycomm3 import Services

from pycomm3 import UDINT
from pycomm3 import DWORD
from pycomm3 import SHORT_STRING
from pycomm3 import STRING
from pycomm3 import DINT
from pycomm3 import BYTE
from pycomm3 import UINT

from pycomm3.cip import n_bytes




def discover_drive_addresses():
    drives = CIPDriver.discover()
    ip_addresses = [drive['ip_address'] for drive in drives]
    return ip_addresses


# multiply by conversion factor on read; divide by factor on set
@dataclass
class Register:
    name: str
    number: int
    data_type: None
    conversion: float
    category: str
    unit: str


registers = {
    'mode': Register('MODE_REG', 2, DINT, 1, 'motor', ''),
    'requested_position': Register('P_SOLL', 3, DINT, 1, 'motor', 'counts'),
    'requested_velocity': Register('V_SOLL', 5, DINT, 0.352, 'motor', 'RPM'),
    'requested_acceleration': Register('A_SOLL', 6, DINT, 270.85, 'motor', 'RPM/s2'),
    'requested_torque': Register('T_SOLL', 7, DINT, 0.293, 'motor', '%'),
    'current_position': Register('P_IST', 10, DINT, 1, 'motor', 'counts'),
    'current_velocity': Register('V_IST_16', 11, DINT, 0.352, 'motor', 'RPM'),
    'P7': Register('P7', 61, DINT, 1, 'motor', 'counts'),
}


class JVLDrive:
    def __init__(self, drive_path):
        self.drive_path = drive_path
        self.connected = self.is_connected()
        self.identity = self.identify_drive()
        self.status = self.identity['status']

    def is_connected(self):
        with CIPDriver(self.drive_path) as drive:
            return drive.connected

    def identify_drive(self):
        with CIPDriver(self.drive_path) as drive:
            return drive.list_identity(self.drive_path)

    def read_register(self, register_name):
        register = registers[register_name]
        if register.category == 'motor':
            class_code = b'\x64'
        else:
            class_code = b'\x65'
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=class_code,
                instance=register.number,
                attribute=b'\x01',
                data_type=register.data_type,
            )
        return param.value * register.conversion, register.unit

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
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x64',
                instance=b'\x02',
                attribute=b'\x01',
                data_type=UDINT,
            )
        return param.value

    def set_operating_mode(self, value):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.set_attribute_single,
                class_code=b'\x64',
                instance=b'\x02',
                attribute=b'\x01',
                request_data=UDINT.encode(value),
            )
        print(param)
        return param

    # I'm still not doing this right....
    def read_assembly_object(self):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x04',
                instance=b'\x65',
                attribute=b'\x03',
                data_type=None,
            )
        return param.value

    def read_current_position(self):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x64',
                instance=b'\x0A',
                attribute=b'\x01',
                data_type=DINT,
            )
        return param.value

    def read_velocity(self):
        velocity = self.read_motor_register(11, data_type=DINT)
        return velocity

    def read_digital_io_register(self):
        with CIPDriver(self.drive_path) as drive:
            param=drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x65',  # module
                instance=b'\x2F',  # register 47
                attribute=b'\x01',
                data_type=DWORD,
            )
        return param.value

    def read_error_register(self):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x64',
                instance=b'\x23', # register 35
                attribute=b'\x01',
                data_type=DWORD,
            )
        return param.value

    def read_module_status_bits(self):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x65',
                instance=b'\x30',  # register 48
                attribute=b'\x01',
                data_type=DWORD,
            )
        return param.value

    def read_control_bits(self):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x64',
                instance=b'\x24',   # register 36
                attribute=b'\x01',
                data_type=DWORD,
            )
        return param.value

    def activate_command_register(self):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.set_attribute_single,
                class_code=b'\x65',
                instance=b'\x0F',
                attribute=b'\x01',
                request_data=UDINT.encode(16777452),
                data_type=UDINT
            )
        return param.value




