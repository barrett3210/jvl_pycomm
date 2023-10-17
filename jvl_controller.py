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

    def issue_general_command(self):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.set_attribute_single,
                class_code=b'\x65',
                instance=UDINT.encode(983040),
                attribute=b'\x01',
            )
        return param

    def set_pos_reg_7(self, value):
        with CIPDriver(self.drive_path) as drive:
            param=drive.generic_message(
                service=Services.set_attribute_single,
                class_code=b'\x64',
                instance=b'\x3D',
                attribute=b'\x01',
                request_data=DINT.encode(value),
                data_type=DINT,
            )
        return param


    def set_requested_position_register(self, value):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.set_attribute_single,
                class_code=b'\x64',
                instance=b'\x03',  # register 3, P_SOLL
                attribute=b'\x01',
                request_data=DINT.encode(value),
                data_type=DINT,
            )
        print(param)
        return param

    def set_maximum_velocity_register(self, value):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.set_attribute_single,
                class_code=b'\x64',
                instance=b'\x05',  # register 5, V_SOLL
                attribute=b'\x01',
                request_data=DINT.encode(value),
                data_type=DINT,
            )
        print("velocty ", value)
        return param

    def read_velocity(self):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x64',
                instance=b'\x0C',
                attribute=b'\x01',
                data_type=DINT,
            )
        return param.value

    def read_torque(self):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x64',
                instance=169,
                data_type=UDINT,
            )
        return param.value

    def read_position_1(self):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x64',
                instance=b'\x31',  # register 49
                attribute=b'\x01',
                data_type=DINT,
            )
        return param.value

    def read_assembly_object(self):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x04',
                instance=b'\x65',
                attribute=b'\x03',
                data_type=DWORD,
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


def read_serial_number_parameter(drive_path):
    with CIPDriver(drive_path) as drive:
        param = drive.generic_message(
            service=Services.get_attribute_single,
            class_code=b'\x01',
            instance=1,
            attribute=6,
            data_type=SHORT_STRING,

        )
    print(param)



