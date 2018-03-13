import os
from time import sleep, time

from PIL import Image

import Adafruit_GPIO.SPI as SPI
import ST7735 as TFT
from gpiozero import Button
from picamera import PiCamera  # camera
from skimage.feature import blob_doh  # blob detection
from skimage.io import imread  # convert jpg to np array

WIDTH = 128
HEIGHT = 160
SPEED_HZ = 125000000

scaleFactor = .25

# Raspberry Pi configuration.
DC = 24
RST = 25
SPI_PORT = 0
SPI_DEVICE = 0
processpoint = [['clear', 'diplay'], ['autoback', 'clear', 'diplay'], [
    'take', 'convert', 'blob find', 'blob to point', 'clear', 'point maths',
    'diplay'
], [
    'autoback', 'take', 'convert', 'blob find', 'blob to point', 'clear',
    'point maths', 'diplay'
]]
averageFps = []
running = 0
tintShade = [32, 32, 32]
tintBack = [255, 255, 255]
tintbuttonvar = 255
mode = 0
debug = 0
disp = 0
draw = 0
camera = 0

buttonTint = Button(2)
buttonMode = Button(3)
buttonDebug = Button(4, hold_time=5)
buttonReset = Button(14, hold_time=2)
buttonexit = Button(15, hold_time=5)


def initlcd():
    global disp, draw
    print 'initilizing lcd'
    disp = TFT.ST7735(
        DC,
        rst=RST,
        spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=SPEED_HZ))
    disp.begin()
    draw = disp.draw()
    disp.display(
        Image.open('pi0toChroma.jpg').rotate(90).resize((WIDTH, HEIGHT)))
    print 'lcd initilized'


def deinitlcd():
    global disp
    disp.display(Image.open('close.jpg').rotate(90).resize((WIDTH, HEIGHT)))
    sleep(.5)
    disp.clear((255, 255, 255))
    disp.display()
    print 'lcd cleared'


def initcamera():
    global camera
    print 'initilizing camera'
    camera = PiCamera()
    camera.color_effects = (128, 128)
    camera.resolution = (int(160 * scaleFactor), int(128 * scaleFactor))
    camera.rotation = 270
    camera.vflip = True
    if debug == 1:
        camera.start_preview()
    print 'camera initilized'


def deinitcamera():
    global camera
    camera.stop_preview()
    camera.close()
    print 'camera closed'


def debugset():
    global debug
    if camera != 0:
        if debug == 0:
            camera.start_preview()
        else:
            camera.stop_preview()
    else:
        print 'camera not defined yet'

    debug ^= 1


def runningstateset(state):
    global running
    try:
        if state.pin.number == 14 and state.is_held:
            state = 1
        elif state.pin.number == 14:
            state = 0
        elif state.pin.number == 15 and state.is_held:
            state = 2
    except:
        print 'error'
        state = runningstateget()
    print state
    running = state


def tintShadeset(tint):
    global tintShade
    tintShade = tint


def tintBackset(tint):
    global tintBack
    tintBack = tint


def tintButton():
    global tintBack, tintbuttonvar
    if tintbuttonvar >= 0:
        tintbuttonvar -= 64
    else:
        tintbuttonvar = 255
    tintBack = [tintbuttonvar, tintbuttonvar, tintbuttonvar]


def modeset(modevar=4):  # 0 manual 1 tint 2 point 3 auto 4 increment
    global mode, averageFps
    if modevar == 4:
        if mode < 3:
            mode += 1
        else:
            mode = 0
    else:
        mode = modevar
    averageFps = []


def runningstateget():
    global running
    return running


def getiso():
    global camera
    maxtint = 4
    iso = float(camera.analog_gain)
    iso = (iso * maxtint)
    iso = (255 - (maxtint * 8)) + iso
    return int(iso)


def halt():
    os.system('sudo halt')


def initbuttons():
    buttonTint.when_pressed = tintButton
    buttonMode.when_pressed = modeset
    buttonDebug.when_pressed = debugset
    buttonDebug.when_held = halt
    buttonReset.when_pressed = runningstateset
    buttonReset.when_held = runningstateset
    buttonexit.when_held = runningstateset


def sandd():
    global averageFps
    initlcd()
    initbuttons()
    initcamera()
    while running != 2:
        while running == 1:
            timer = []
            points = []
            modeinternal = mode

            if (modeinternal == 1) or (modeinternal == 3):
                timer.append(time())
                ti = getiso()
                tintBackset([ti, ti, ti])

            if modeinternal >= 2:
                timer.append(time())

                camera.capture(
                    'image1.jpg', use_video_port=True, thumbnail=None)

                timer.append(time())
                img1 = imread('image1.jpg', as_grey=True)

                timer.append(time())
                blobs_doh = blob_doh(img1, max_sigma=15, threshold=.0075)

                timer.append(time())

                for i in range(len(blobs_doh)):
                    points.append([
                        blobs_doh[i][0] / scaleFactor,
                        blobs_doh[i][1] / scaleFactor,
                        (blobs_doh[i][1] / 3) / scaleFactor, tintShade
                    ])

            timer.append(time())

            disp.clear((tintBack[2], tintBack[1], tintBack[0]))

            if modeinternal >= 2:
                timer.append(time())
                for i in range(0, len(points)):
                    x1 = int(points[i][0] - points[i][2])
                    x2 = int(points[i][0] + points[i][2])
                    y1 = int(points[i][1] - points[i][2])
                    y2 = int(points[i][1] + points[i][2])
                    draw.ellipse(
                        (x1, y1, x2, y2),
                        fill=(points[i][3][2], points[i][3][1],
                              points[i][3][0]))

            timer.append(time())

            disp.display()

            timer.append(time())

            if debug == 1:

                print 'number of points: {}\n'.format(len(points))
                print 'background tint: {}\n'.format(tintBack)
                print 'foreground tint: {}\n'.format(tintShade)
                for t in range(0, len(timer) - 1):
                    print 'function {} : time {}\n'.format(
                        processpoint[modeinternal][t], timer[t + 1] - timer[t])

                totaltime = timer[len(timer) - 1] - timer[0]
                averageFps.append(1 / totaltime)
                if len(averageFps) >= 11:
                    if len(averageFps) >= 61:
                        averageFps.pop(0)
                    print 'average fps = {: 4.2f}\n'.format(
                        sum(averageFps) / len(averageFps))
                print 'total = {: 4.2f}  fps = {: 4.2f}\n'.format(
                    totaltime, averageFps[len(averageFps) - 1])

        sleep(1)

    deinitlcd()
    deinitcamera()
