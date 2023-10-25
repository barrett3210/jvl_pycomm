from enum import Enum

read_assembly = {}
requested_items = None
in_position = False
homed = False
my_in_position = False
enable_drive = False
requested_mode = 0
options_text = "0"

callback = None

move_down_distance = 2.5

min_position_counts = 10000

insertion_stops = [1.0, 2.0, 4.0, 6.0]
insertion_interrupt = False
insertion_start_position = 0.0
spectra_done = False
insertion_in_progress = False
insertion_step_count = 0

class Convert(Enum):
    COUNT2CM = 0.0000206809
    CM2COUNT = 48353.795
    CMSEC2VELOCITY = 1005.7574
    VELOCITY2CMSEC = 0.00099428
    PCT2TORQUE = 3.41
    TORQUE2PCT = 0.293255132

startup_register_values = {
    5: int(0.25 * Convert.CMSEC2VELOCITY.value),  # Req. velocity
    6: int(4875 / 270),  # Req. acceleration
    7: int(30 * Convert.PCT2TORQUE.value),  # Req. torque
    38: 0,  # Homing position
    40: -int(0.12 * Convert.CMSEC2VELOCITY.value),  # Homing velocity
    41: int(30 * Convert.PCT2TORQUE.value),  # Homing torque
}
