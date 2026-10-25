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
# px of the panel hidden behind the frame, measured with the calibration pattern
MARGIN_LEFT = 48
MARGIN_TOP = 13
MARGIN_RIGHT = 45
MARGIN_BOTTOM = 8
# zoom to fill the visible area if that crops at most this fraction of the photo,
# otherwise show the whole photo with black bars (1.0 = always fill, 0.0 = never crop)
MAX_CROP = 1.0
BORDER_COLOR = (0, 0, 0)
RESAMPLING = Image.BICUBIC

VISIBLE = (RESOLUTION[0] - MARGIN_LEFT - MARGIN_RIGHT,
           RESOLUTION[1] - MARGIN_TOP - MARGIN_BOTTOM)

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
image = ImageOps.exif_transpose(Image.open(photo)).convert('RGB')

# how much of the photo would be cut off to fill the visible area
image_ratio = image.width / image.height
visible_ratio = VISIBLE[0] / VISIBLE[1]
crop = 1 - min(image_ratio, visible_ratio) / max(image_ratio, visible_ratio)

canvas = Image.new('RGB', RESOLUTION, BORDER_COLOR)
if crop <= MAX_CROP:
    # zoom to fill the visible area; the overflow runs into the hidden margins instead of being cut
    scale = max(VISIBLE[0] / image.width, VISIBLE[1] / image.height)
else:
    # whole photo inside the visible area, black bars
    scale = min(VISIBLE[0] / image.width, VISIBLE[1] / image.height)
print('Crop {:.0%} -> {}'.format(crop, 'fill' if crop <= MAX_CROP else 'fit with bars'))
# same scale for width and height, so the photo is never skewed
fitted = image.resize((round(image.width * scale), round(image.height * scale)), RESAMPLING)
# center on the visible area (not the panel, since the margins aren't symmetric)
canvas.paste(fitted, (round(MARGIN_LEFT + VISIBLE[0] / 2 - fitted.width / 2),
                      round(MARGIN_TOP + VISIBLE[1] / 2 - fitted.height / 2)))

epd.init()
epd.display(epd.getbuffer(canvas))
epd.sleep() # power the panel down while the image is held
epd7in3e.epdconfig.module_exit(cleanup=True)

with open(LAST_PHOTO_FILE, 'w') as f:
    f.write(photo)
