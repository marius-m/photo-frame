#!/usr/bin/env python3

import glob
import random
import os
import sys
from PIL import Image, ImageOps

sys.path.append(os.path.expanduser('~/Projects/random/RaspberryPi_JetsonNano/python/lib'))
from waveshare_epd import epd7in3e

epd = epd7in3e.EPD()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTO_PATH = os.path.join(CURRENT_DIR, 'images')
LAST_PHOTO_FILE = os.path.join(CURRENT_DIR, '.last-photo')
RESOLUTION = (epd.width, epd.height)  # 800x480
BORDER_COLOR = (255, 255, 255)
RESAMPLING = Image.BICUBIC

photos = glob.glob(PHOTO_PATH + '/*.jpg')
if not photos:
    print(f"Error: no .jpg images found in '{PHOTO_PATH}'.")
    sys.exit(1)

# avoid showing the same photo twice in a row
try:
    with open(LAST_PHOTO_FILE) as f:
        last_photo = f.read().strip()
except FileNotFoundError:
    last_photo = None
photo = random.choice([p for p in photos if p != last_photo] or photos)

print('Display {}'.format(photo))
image = Image.open(photo).convert('RGB')
# resizedimage = ImageOps.pad(image, RESOLUTION, RESAMPLING, BORDER_COLOR)
resizedimage = ImageOps.fit(image, RESOLUTION, RESAMPLING)
epd.init()
epd.display(epd.getbuffer(resizedimage))
epd.sleep() # power the panel down while the image is held
epd7in3e.epdconfig.module_exit(cleanup=True)

with open(LAST_PHOTO_FILE, 'w') as f:
    f.write(photo)
