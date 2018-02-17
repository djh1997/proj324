from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ST7735 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

import picamera  # camera
from time import sleep, time
from skimage.feature import blob_doh  # blob detection
from skimage.io import imread  # convert jpg to np array


WIDTH = 128
HEIGHT = 160
SPEED_HZ = 640000000

scaleFactor = .5

# Raspberry Pi configuration.
DC = 24
RST = 25
SPI_PORT = 0
SPI_DEVICE = 0
process = ['take', 'convert', 'blob find',
           'blob to point', 'clear', 'point maths', 'diplay']
points = []
running = 0
tintShade = [32, 32, 32]
tintBack = [255, 255, 255]


def initlcd():
    global disp, draw
    disp = TFT.ST7735(
        DC,
        rst=RST,
        spi=SPI.SpiDev(
            SPI_PORT,
            SPI_DEVICE,
            max_speed_hz=SPEED_HZ))
    disp.begin()
    draw = disp.draw()


def initcamera():
    global camera
    camera = picamera.PiCamera()
    camera.color_effects = (128, 128)
    camera.resolution = (int(160 * scaleFactor), int(128 * scaleFactor))
    camera.start_preview()


def deinitcamera():
    global camera
    camera.stop_preview()
    camera.close()
    print('camera closed')


def runningstateset(state):
    global running
    running = state


def tintShadeset(tint):
    global tintShade
    tintShade = tint


def tintBackset(tint):
    global tintBack
    tintBack = tint


def runningstateget():
    global running
    return(running)


def sandd():
    global running, tintShade
    initlcd()
    initcamera()
    while running != 2:
        while running == 1:
            print(tintShade)
            print(tintBack)
            timer = []
            timer.append(time())  # t1

            camera.capture('image1.jpg')  # 0.5

            timer.append(time())  # t2

            img1 = imread('image1.jpg', as_grey=True)  # 0.06

            timer.append(time())  # t3

            blobs_doh = blob_doh(img1, max_sigma=15, threshold=.0075)  # .44

            timer.append(time())  # t4

            points = []
            for i in range(len(blobs_doh)):  # 0.0002
                points.append([blobs_doh[i][0] / scaleFactor, blobs_doh[i]
                               [1] / scaleFactor, (blobs_doh[i][1] / 3) / scaleFactor, tintShade])

            timer.append(time())  # t6

            disp.clear((tintBack[2], tintBack[1], tintBack[0]))  # 0.036

            timer.append(time())  # t7

            for i in range(0, len(points)):  # 0.0019

                x1 = int(points[i][0] - points[i][2])
                x2 = int(points[i][0] + points[i][2])
                y1 = int(points[i][1] - points[i][2])
                y2 = int(points[i][1] + points[i][2])
                draw.ellipse((x1, y1, x2, y2), fill=(
                    points[i][3][2], points[i][3][1], points[i][3][0]))

            timer.append(time())  # t8

            disp.display()  # 0.13

            timer.append(time())  # t9

            # print(points)
            #
            # for t in range(0, len(timer) - 1):
            #     print('function {} : time {}'.format(
            #         process[t], timer[t + 1] - timer[t]))

            print('total')
            print(timer[len(timer) - 1] - timer[0])
        sleep(1)
    deinitcamera()
