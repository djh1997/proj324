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
pointtoggle = 1


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


def pointtoggleset():
    global pointtoggle
    pointtoggle ^= 1


def runningstateget():
    global running
    return(running)


def sandd():
    global running, tintShade
    initlcd()
    initcamera()
    while running != 2:
        while running == 1:
            if pointtoggle == 1:
                camera.capture('image1.jpg')
                img1 = imread('image1.jpg', as_grey=True)
                blobs_doh = blob_doh(img1, max_sigma=15, threshold=.0075)
                points = []

                for i in range(len(blobs_doh)):
                    points.append([blobs_doh[i][0] / scaleFactor, blobs_doh[i]
                                   [1] / scaleFactor, (blobs_doh[i][1] / 3) / scaleFactor, tintShade])

            disp.clear((tintBack[2], tintBack[1], tintBack[0]))

            if pointtoggle == 1:
                for i in range(0, len(points)):
                    x1 = int(points[i][0] - points[i][2])
                    x2 = int(points[i][0] + points[i][2])
                    y1 = int(points[i][1] - points[i][2])
                    y2 = int(points[i][1] + points[i][2])
                    draw.ellipse((x1, y1, x2, y2), fill=(
                        points[i][3][2], points[i][3][1], points[i][3][0]))

            disp.display()

        sleep(1)

    deinitcamera()
