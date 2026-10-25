import os
import sys
from PIL import Image, ImageDraw

sys.path.append(os.path.expanduser('~/Projects/random/RaspberryPi_JetsonNano/python/lib'))
from waveshare_epd import epd7in3e

MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT, MARGIN_BOTTOM = 48, 13, 45, 8  # <- measured values

epd = epd7in3e.EPD()
W, H = epd.width, epd.height
img = Image.new('RGB', (W, H), (0, 0, 0))
draw = ImageDraw.Draw(img)
box = [MARGIN_LEFT, MARGIN_TOP, W - 1 - MARGIN_RIGHT, H - 1 - MARGIN_BOTTOM]
draw.rectangle(box, fill=(255, 255, 255), outline=(255, 0, 0), width=2)

epd.init()
epd.display(epd.getbuffer(img))
epd.sleep()
epd7in3e.epdconfig.module_exit(cleanup=True)
print(f'Visible area: {W - MARGIN_LEFT - MARGIN_RIGHT}x{H - MARGIN_TOP - MARGIN_BOTTOM}')
