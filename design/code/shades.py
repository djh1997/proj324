import os
from time import sleep, time

from PIL import Image

import Adafruit_GPIO.SPI as SPI
import ST7735 as TFT
from gpiozero import Button
from picamera import PiCamera  # camera
from skimage.feature import blob_doh  # blob detection
from skimage.io import imread  # convert jpg to np array

# screen variables
WIDTH = 128
HEIGHT = 160
SPEED_HZ = 125000000

scaleFactor = .25

# Raspberry Pi configuration.
DC = 24
RST = 25
SPI_PORT = 0
SPI_DEVICE = 0

# program variables
processpoint = [['clear', 'display'], ['autoback', 'clear', 'display'], [
    'take', 'convert', 'blob find', 'blob to point', 'clear', 'point maths',
    'display'
], [
    'autoback', 'take', 'convert', 'blob find', 'blob to point', 'clear',
    'point maths', 'display'
]]
averageFps = []
running = 0
tintShade = [32, 32, 32]
tintBack = [256, 256, 256]
tintbuttonvar = 255
mode = 0
debug = 0
disp = 0
draw = 0
camera = 0

# button connection
buttonTint = Button(2)
buttonMode = Button(3)
buttonDebug = Button(4, hold_time=5)
buttonReset = Button(14, hold_time=2)
buttonexit = Button(15, hold_time=5)


def initlcd():  # initilize the lcd's
    global disp, draw
    print 'initializing LCD'
    disp = TFT.ST7735(
        DC,
        rst=RST,
        spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE,
                       max_speed_hz=SPEED_HZ))  # setup SPI port
    disp.begin()  # start screen class
    disp.display(
        Image.open('pi0toChroma.jpg').rotate(270).transpose(
            Image.FLIP_TOP_BOTTOM).resize((WIDTH,
                                           HEIGHT)))  # draw splash screen
    draw = disp.draw()  # put splash screen on LCD's
    print 'LCD initialized'


def deinitlcd():
    global disp
    disp.display(Image.open('close.jpg').rotate(90).resize(
        (WIDTH, HEIGHT)))  # display close screen
    sleep(.5)
    disp.clear((256, 256, 256))  # set LCD to clear
    disp.display()
    print 'LCD cleared'


def initcamera():
    global camera
    print 'initializing camera'
    camera = PiCamera()  # open camera
    camera.color_effects = (128, 128)  # set camera to grey scale
    camera.resolution = (int(160 * scaleFactor),
                         int(128 * scaleFactor))  # set resolution to screens
    camera.rotation = 270  # correct orinetation
    camera.vflip = True
    if debug == 1:  # incase debug was called before camera initialization was run
        camera.start_preview()  # start camera preview
    sleep(3)  # wait for camera to stabilise
    print 'camera initialized'


def deinitcamera():
    # disconnect camera so the next instance of the program can access it
    global camera
    camera.close()
    print 'camera closed'


def debugset():
    global debug
    if camera != 0:  # check if camera initialization has been run
        if debug == 0:  # toggle preview
            camera.start_preview()
        else:
            camera.stop_preview()
    else:
        print 'camera not defined yet'  # if camera initialization hasn't  been run print warning

    debug ^= 1
    if debug == 1:
        print 'debug on'
    else:
        print 'debug off'


def runningstateset(state):
    global running
    try:  # try assuming state is a button
        if state.pin.number == 14 and state.is_held:  # if state button is held
            state = 1  # set state to running
        elif state.pin.number == 14:  # if state button is pressed
            state = 0  # set state to stopped
        elif state.pin.number == 15 and state.is_held:  # if exit button is held
            state = 2  # set state to exit
    except AttributeError:  # catch not button error
        print 'not button'  # print warning
    print 'state ' + str(state)  # print new state
    running = state  # set state


def tintShadeset(tint):
    global tintShade
    tintShade = tint  # set tint level for active shade points


def autoshadeset(tintdifference):
    global tintShade
    for i in range(len(tintShade)):
        tintShade[
            i] = tintBack[i] - tintdifference  # set tint difference points


def tintBackset(tint):
    global tintBack
    tintBack = tint  # set tint level for background


def tintButton(buttonTint):
    global tintBack, tintbuttonvar
    if buttonTint.is_held or tintbuttonvar < 64:  # if tint button is held reset tint to clear
        tintbuttonvar = 256  # set tint to clear
    elif tintbuttonvar >= 64:  # increment tint if not at limit
        tintbuttonvar -= 64
    tintBack = [tintbuttonvar, tintbuttonvar,
                tintbuttonvar]  # format tint correctly
    print tintBack


def modeset(modevar):  # 0 manual 1 tint 2 point 3 auto 4 increment
    global mode, averageFps
    try:  # try assuming modevar is a button
        if modevar.pin.number == 3 and modevar.is_held:  # if mode button is held
            modevar = 0  # reset mode to manual
        elif modevar.pin.number == 3:  # if mode button is pressed
            if mode >= 3:  # if at limit the reset to manual
                modevar = 0
            else:  # else increment
                modevar = mode + 1
    except AttributeError:  # catch not button error
        print 'not button'  # print warning
    mode = modevar  # set mode
    print 'mode ' + str(mode)  # display new mode
    averageFps = []  # reset average fps array


def runningstateget():  # function for telegram to retrieve current state
    global running
    return running


def getiso():
    global camera
    maxtint = 4
    iso = float(camera.analog_gain)  # get current ambient brightness 0..8
    iso = (iso * maxtint)  # adjust buy max tint level
    iso = (256 - (maxtint * 8)) + iso  # clear - max tint + ISO tint
    return int(iso)


def halt():
    os.system('sudo halt')  # send halt command to terminal


def initbuttons():
    buttonTint.wait_for_release(
    )  # wait incase any of the buttons are locked high
    buttonMode.wait_for_release()
    buttonDebug.wait_for_release()
    buttonReset.wait_for_release()
    buttonexit.wait_for_release()
    buttonTint.when_pressed = tintButton  # set button state to correct function
    buttonTint.when_held = tintButton
    buttonMode.when_pressed = modeset
    buttonMode.when_held = modeset
    buttonDebug.when_pressed = debugset
    # buttonDebug.when_held = halt
    buttonReset.when_pressed = runningstateset
    buttonReset.when_held = runningstateset
    # buttonexit.when_held = runningstateset


def sandd():
    global averageFps
    initlcd()  # initialize peripherals
    initbuttons()
    initcamera()
    while running != 2:  # exit state
        while running == 1:  # running state
            timer = []  # reset internal variables
            points = []
            modeinternal = mode

            if (modeinternal == 1) or (
                    modeinternal == 3):  # if mode with auto background tint
                timer.append(time())  # add timer point
                ti = getiso()  # get light level
                tintBackset([ti, ti, ti])  # calculate background tint
                if modeinternal == 3:
                    autoshadeset(ti)

            if modeinternal >= 2:  # if active point shading mode
                timer.append(time())  # add timer point

                camera.capture(
                    'image1.jpg', use_video_port=True,
                    thumbnail=None)  # capture image

                timer.append(time())  # add timer point
                img1 = imread('image1.jpg', as_grey=True)

                timer.append(time())  # add timer point
                blobs_doh = blob_doh(
                    img1, max_sigma=15, threshold=.0075)  # find blobs

                timer.append(time())  # add timer point

                for i in range(len(blobs_doh)):  # calculate points from blobs
                    points.append([
                        blobs_doh[i][0] / scaleFactor,
                        blobs_doh[i][1] / scaleFactor,
                        (blobs_doh[i][1] / 3) / scaleFactor, tintShade
                    ])  # x,y,r,tint

            timer.append(time())  # add timer point

            disp.clear((tintBack[2], tintBack[1],
                        tintBack[0]))  # set background tint

            if modeinternal >= 2:  # if active point shading mode
                timer.append(time())  # add timer point
                for i in range(0,
                               len(points)):  # convert x,y,r to bounding box
                    x1 = int(points[i][0] - points[i][2])
                    x2 = int(points[i][0] + points[i][2])
                    y1 = int(points[i][1] - points[i][2])
                    y2 = int(points[i][1] + points[i][2])
                    draw.ellipse(
                        (x1, y1, x2, y2),
                        fill=(points[i][3][2], points[i][3][1],
                              points[i][3][0]))  # draw

            timer.append(time())  # add timer point

            disp.display()  # put the drawing on the the LCD's

            timer.append(time())  # add timer point

            if debug == 1:  # if debug is on the print timings

                print 'number of points: {}\n'.format(len(points))
                print 'background tint: {}\n'.format(tintBack)
                print 'foreground tint: {}\n'.format(tintShade)
                for t in range(0,
                               len(timer) -
                               1):  # iterate over timing list to get timings
                    print 'function {} : time {}\n'.format(
                        processpoint[modeinternal][t],
                        timer[t + 1] - timer[t])  # print function and time

                totaltime = timer[len(timer)
                                  - 1] - timer[0]  # calculate total time
                averageFps.append(1 / totaltime)  # calculate fps and append
                if len(averageFps) >= 11:  # buffer has min number of values
                    if len(averageFps) >= 61:  # buffer full then remove oldest
                        averageFps.pop(0)
                    print 'average fps = {: 4.2f}\n'.format(
                        sum(averageFps) / len(averageFps))  # print average fps
                print 'total = {: 4.2f}  fps = {: 4.2f}\n'.format(
                    totaltime, averageFps[len(averageFps)
                                          - 1])  # print total time and fps

        sleep(1)

    deinitlcd()  # close peripherals
    deinitcamera()
