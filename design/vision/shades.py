# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ST7735 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

from random import randint
import picamera
import picamera.array
from time import sleep, time
from math import sqrt
from skimage import data
from skimage.feature import blob_doh
from skimage.io import imread

WIDTH = 128
HEIGHT = 160
SPEED_HZ = 640000000

# Raspberry Pi configuration.
DC = 24
RST = 25
SPI_PORT = 0
SPI_DEVICE = 0

points=[]

disp = TFT.ST7735(
    DC,
    rst=RST,
    spi=SPI.SpiDev(
        SPI_PORT,
        SPI_DEVICE,
        max_speed_hz=SPEED_HZ))

camera = picamera.PiCamera()
camera.color_effects=(128,128)
camera.resolution = (160,128)
camera.start_preview()

for k in range(100):
    print(k)
    start=time()
    camera.capture('image1.jpg')
    img1=imread('image1.jpg',as_grey=True)

    blobs_doh = blob_doh(img1, max_sigma=30, threshold=.01)
    points=[]
    for i in range(len(blobs_doh)):
        points.append([blobs_doh[i][0],blobs_doh[i][1],blobs_doh[i][1]/2,50])

    print(points)
    print('@')
    # Initialize display.
    disp.begin()
    disp.clear((255,255,255))
    draw = disp.draw()

    for i in range(0,len(points)):

        x1=int(points[i][0]-points[i][2])
        x2=int(points[i][0]+points[i][2])
        y1=int(points[i][1]-points[i][2])
        y2=int(points[i][1]+points[i][2])
        colour=int(2.55*points[i][3])
        draw.ellipse((x1,y1,x2,y2),fill=(colour,colour,colour))

    disp.display()
    end=time()
    print(end-start)



camera.stop_preview()
camera.close()
