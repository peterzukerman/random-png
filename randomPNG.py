#!/usr/bin/python3
import sys
import requests 
from math import ceil
from PIL import Image #python3 -m pip install --upgrade Pillow

URL = "https://www.random.org/integers/?num={}&min={}&max={}&col={}&base={}&format={}&rnd=new"

COLS_IN_RESPONSE = 3 # more convenient, allows conversion to RGB as a tuple

#will require 4.5 -> 5 api requests. 120*120*3 = 43200 random rgb values to generate
#limit of 10000, so each fetch will be of 10000 random numbers
#works for any width/height
def createRandomPixels(URL, width, height,
                randomNumbersPerRequest=9999,   #must be under 10k generation limit, divisible by 3
                minRGB=0, 
                maxRGB=255, #rgb from 0-255
                col_delimiter = '\t',
                base=10, 
                formatting='plain'): #txt easier to parse

    totalRandomNumbers = width * height * 3

    pixels = []

    for _ in range(ceil(totalRandomNumbers / randomNumbersPerRequest)):
        #example: for 120*120 = 43200 / 10000 = 5 requests
        url = URL.format(randomNumbersPerRequest, minRGB, maxRGB, COLS_IN_RESPONSE, base, formatting)
        r = requests.get(url) 
        for line in r.text.splitlines():
            (r,g,b) = tuple(line.split(col_delimiter))
            pixels.append((int(r),int(g),int(b)))

    return pixels

def generatePNG(w, h):
    pixels = createRandomPixels(URL, w, h)
    img = Image.new('RGB', (w, h))
    data = img.load()
    curr = 0
    for y in range(h):
        for x in range(w):
            data[(x, y)] = pixels[curr]
            curr += 1
    img.save('random.png')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: ./randomPNG width height')
        sys.exit(0)
    else:
        generatePNG(int(sys.argv[1]), int(sys.argv[2]))