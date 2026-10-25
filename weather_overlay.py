#!/usr/bin/env python3
# Draws the current weather (Open-Meteo) as outlined text in the bottom-left corner of the visible area.
# Used by gallery-run.py; run directly to render weather-preview.png without the panel.

import json
import os
import sys
import time
import urllib.parse
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageOps

LATITUDE = 54.69   # Vilnius
LONGITUDE = 25.28
TIMEZONE = 'Europe/Vilnius'
API_URL = 'https://api.open-meteo.com/v1/forecast'
TIMEOUT = 10  # seconds
CACHE_MAX_AGE = 3 * 3600  # use the last good response for up to 3 h when offline

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(CURRENT_DIR, '.weather-cache.json')

TEXT_COLOR = (255, 255, 255)
OUTLINE_COLOR = (0, 0, 0)  # no background box; the outline keeps the text readable on any photo
OUTLINE_WIDTH = 2
PADDING = 10
FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_SIZE = 28

# Open-Meteo weather_code (WMO) -> short description
WMO_CODES = {
    0: 'Clear', 1: 'Mostly clear', 2: 'Partly cloudy', 3: 'Overcast',
    45: 'Fog', 48: 'Fog',
    51: 'Light drizzle', 53: 'Drizzle', 55: 'Heavy drizzle',
    56: 'Freezing drizzle', 57: 'Freezing drizzle',
    61: 'Light rain', 63: 'Rain', 65: 'Heavy rain',
    66: 'Freezing rain', 67: 'Freezing rain',
    71: 'Light snow', 73: 'Snow', 75: 'Heavy snow', 77: 'Snow grains',
    80: 'Rain showers', 81: 'Rain showers', 82: 'Heavy showers',
    85: 'Snow showers', 86: 'Snow showers',
    95: 'Thunderstorm', 96: 'Thunderstorm, hail', 99: 'Thunderstorm, hail',
}


def fetch_weather():
    """Current weather, falling back to a recent cached response."""
    params = urllib.parse.urlencode({
        'latitude': LATITUDE,
        'longitude': LONGITUDE,
        'current': 'temperature_2m,weather_code',
        'timezone': TIMEZONE,
        'forecast_days': 1,
    })
    try:
        with urllib.request.urlopen(API_URL + '?' + params, timeout=TIMEOUT) as response:
            data = json.load(response)
        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f)
        return data
    except (OSError, ValueError) as e:
        print('Weather fetch failed: {}'.format(e))
    try:
        if time.time() - os.path.getmtime(CACHE_FILE) <= CACHE_MAX_AGE:
            with open(CACHE_FILE) as f:
                print('Using cached weather')
                return json.load(f)
    except (OSError, ValueError):
        pass
    return None


def load_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except OSError:
        return ImageFont.load_default(size=size)


def draw_weather(canvas, box):
    """Draw the current weather in the bottom-left corner of box = (left, top, right, bottom)."""
    data = fetch_weather()
    if data is None:
        print('No weather data, skipping overlay')
        return

    current = data['current']
    text = '{:.0f}°C  {}'.format(current['temperature_2m'],
                                 WMO_CODES.get(current['weather_code'], '')).strip()
    left, top, right, bottom = box
    draw = ImageDraw.Draw(canvas)
    draw.text((left + PADDING, bottom - PADDING), text, font=load_font(FONT_SIZE),
              fill=TEXT_COLOR, stroke_width=OUTLINE_WIDTH, stroke_fill=OUTLINE_COLOR, anchor='ld')
    print('Weather: {}'.format(text))


if __name__ == '__main__':
    # preview: python3 weather_overlay.py [photo.jpg] -> weather-preview.png
    # margins copied from gallery-run.py
    resolution = (800, 480)
    box = (48, 13, 800 - 45, 480 - 8)
    canvas = Image.new('RGB', resolution, (128, 128, 128))
    if len(sys.argv) > 1:
        photo = ImageOps.exif_transpose(Image.open(sys.argv[1])).convert('RGB')
        visible = (box[2] - box[0], box[3] - box[1])
        canvas.paste(ImageOps.fit(photo, visible, Image.BICUBIC), box[:2])
    draw_weather(canvas, box)
    preview = os.path.join(CURRENT_DIR, 'weather-preview.png')
    canvas.save(preview)
    print('Saved {}'.format(preview))
