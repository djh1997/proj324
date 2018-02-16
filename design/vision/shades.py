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

scaleFactor=4

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
camera.resolution = (160*scaleFactor,128*scaleFactor)
camera.start_preview()

disp.begin()
draw = disp.draw()

for k in range(100):
    print(k)
    timer=[]
    timer.append(time())#t1

    camera.capture('image1.jpg')#0.5

    timer.append(time())#t2

    img1=imread('image1.jpg',as_grey=True)#0.06

    timer.append(time())#t3

    blobs_doh = blob_doh(img1, max_sigma=30, threshold=.01)#.44

    timer.append(time())#t4

    points=[]
    for i in range(len(blobs_doh)):#0.0002
        points.append([blobs_doh[i][0]/scaleFactor,blobs_doh[i][1]/scaleFactor,(blobs_doh[i][1]/2)/scaleFactor,50])

    timer.append(time())#t6

    disp.clear((255,255,255))#0.036



    timer.append(time())#t7

    for i in range(0,len(points)):#0.0019

        x1=int(points[i][0]-points[i][2])
        x2=int(points[i][0]+points[i][2])
        y1=int(points[i][1]-points[i][2])
        y2=int(points[i][1]+points[i][2])
        colour=int(2.55*points[i][3])
        draw.ellipse((x1,y1,x2,y2),fill=(colour,colour,colour))

    timer.append(time())#t8

    disp.display()#0.13

    timer.append(time())#t9

    print(points)

    for t in range(0,len(timer)-1):
        print(timer[t+1]-timer[t])

    print('total')
    print(timer[len(timer)-1]-timer[0])

camera.stop_preview()
camera.close()
