import time
import datetime

import config


def simulate_spectrometer_action():
    time.sleep(0.5)
    now = datetime.datetime.now().time()
    position = f"{config.read_assembly['position'] * config.Convert.COUNT2CM.value:0.2f} cm"
    print("**Spectrum** ", now, position)
    config.spectra_done = True
    return (position, now)