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


    def get_operating_mode(self):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x64',
                instance=b'\x02',
                attribute=b'\x01',
                # data_type=UDINT(n_bytes(1))
                data_type=UDINT,
                # data_type=None
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
                # data_type=UDINT,
                # connected=True,
            )
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
                request_data=UDINT.encode(value),
                data_type=UDINT,
            )
        return param

    def read_velocity(self):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x64',
                instance=b'\x0C',
                attribute=b'\x01',
                data_type=UDINT,
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


    def read_assembly_object(self):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x04',
                instance=b'\x65',
                attribute=b'\x04',
                data_type=None,

            )
            return param


    def read_current_position(self):
        with CIPDriver(self.drive_path) as drive:
            param = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x64',
                instance=b'\x0A',
                attribute=b'\x01',
                data_type=UDINT,
            )
        return param.value

    def read_assembly_object(self):
        with CIPDriver(self.drive_path) as drive:
            param=drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x64',
                instance=b'\x23',
                attribute=b'\x01',
                data_type=DWORD,
            )
        return param

    def read_digital_io_register(self):
        with CIPDriver(self.drive_path) as drive:
            param=drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x65',  # module
                instance=b'\x10', # b'\x2F',  # register 47
                attribute=b'\x01',
                data_type=DWORD,
            )



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


def send_a_message(ip_address):
    with CIPDriver(ip_address) as drive:
        try:
            response = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x64',
                instance=b'\x02',
                attribute=b'\x0C',
                data_type=None,
            )
            return response

        except Exception as e:
            print("raised an exception")
            print(e)


# from top of p. 86
def read_operating_mode(ip_address):
    with CIPDriver(ip_address) as drive:
        try:
            response = drive.generic_message(
                service=Services.get_attribute_single,
                class_code=b'\x64', # pre-configured motor register
                instance=b'\x02', # Mode register in the motor
                attribute=b'\x01',
                data_type=None,
            )
            return response

        except Exception as e:
            print("raised an exception")
            print(e)