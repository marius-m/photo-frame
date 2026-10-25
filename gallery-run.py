#!/usr/bin/env python3

import glob
import time
import random
import os
import sys
from PIL import Image, ImageOps

sys.path.append(os.path.expanduser('~/Projects/random/RaspberryPi_JetsonNano/python/lib'))
from waveshare_epd import epd7in3e

epd = epd7in3e.EPD()

MIN_SLEEP = 600
MAX_SLEEP = 3600

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTO_PATH = os.path.join(CURRENT_DIR, 'images')
RESOLUTION = (epd.width, epd.height)  # 800x480
BORDER_COLOR = (255, 255, 255)
RESAMPLING = Image.BICUBIC

if not os.path.exists(PHOTO_PATH):
    print(f"Error: Photo directory '{PHOTO_PATH}' does not exist.")
    print("Please create the directory and add PNG images before running the script.")
    sys.exit(1)

try:
  while True:
    print('Reloading list of images')
    photos = glob.glob(PHOTO_PATH + '/*.jpg')
    random.shuffle(photos)
    print('Pictures in list: {}'.format(len(photos)))
    for photo in photos:
      print('Display {}'.format(photo))
      image = Image.open(photo).convert('RGB')
      # resizedimage = ImageOps.pad(image, RESOLUTION, RESAMPLING, BORDER_COLOR)
      resizedimage = ImageOps.fit(image, RESOLUTION, RESAMPLING)
      epd.init()
      epd.display(epd.getbuffer(resizedimage))
      epd.sleep() # power the panel down while the image is held
      time.sleep(random.randint(MIN_SLEEP, MAX_SLEEP)) # keep image on screen between MIN_SLEEP and MAX_SLEEP seconds before changing (random per image)
    time.sleep(5) # sleep to not overload the PI when e.g. no images are found
except KeyboardInterrupt:
  epd7in3e.epdconfig.module_exit(cleanup=True)
