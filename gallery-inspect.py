import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.path.append(os.path.expanduser('~/Projects/random/RaspberryPi_JetsonNano/python/lib'))
from waveshare_epd import epd7in3e

START, STEP, END = 0, 10, 80   # px from the edge; narrow down later, e.g. 20, 2, 40

epd = epd7in3e.EPD()
W, H = epd.width, epd.height
img = Image.new('RGB', (W, H), (255, 255, 255))
draw = ImageDraw.Draw(img)
try:
    font = ImageFont.load_default(size=8)
except TypeError:  # Pillow < 10.1
    font = ImageFont.load_default()
colors = [(255, 0, 0), (0, 0, 255), (0, 0, 0)]

for i, d in enumerate(range(START, END + 1, STEP)):
    c = colors[i % len(colors)]
    draw.rectangle([d, d, W - 1 - d, H - 1 - d], outline=c)
    off = 40 + i * 30  # stagger labels along each edge so they don't overlap
    draw.text((off, d + 1), str(d), fill=c, font=font)            # top
    draw.text((off, H - 1 - d - 9), str(d), fill=c, font=font)    # bottom
    draw.text((d + 2, off), str(d), fill=c, font=font)            # left
    draw.text((W - 1 - d - 16, off), str(d), fill=c, font=font)   # right

epd.init()
epd.display(epd.getbuffer(img))
epd.sleep()
epd7in3e.epdconfig.module_exit(cleanup=True)
print(f'Drew {START}..{END} px every {STEP} px on {W}x{H}')
