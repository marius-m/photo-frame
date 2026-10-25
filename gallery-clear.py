#!/usr/bin/env python3

import os
import sys

sys.path.append(os.path.expanduser('~/Projects/random/RaspberryPi_JetsonNano/python/lib'))
from waveshare_epd import epd7in3e

epd = epd7in3e.EPD()

print('Clearing screen to white')
epd.init()
epd.Clear()
epd.sleep() # power the panel down
epd7in3e.epdconfig.module_exit(cleanup=True)
print('Done, safe to power off')
