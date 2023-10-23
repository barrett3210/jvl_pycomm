from enum import Enum

read_assembly = {}
requested_items = None
in_position = False

move_down_distance = 2.5


class Convert(Enum):
    COUNT2CM = 0.0000206809
    CM2COUNT = 48353.795
    CMSEC2VELOCITY = 1005.7574
    VELOCITY2CMSEC = 0.00099428
    PCT2TORQUE = 3.41
    TORQUE2PCT = 0.293255132
