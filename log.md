# Tasks

-   [x] get camera working
-   [x] get pi connected over WiFi
-   [x] get LCD connected
-   [x] get raw data from camera for processing
-   [x] get raw brightness from LDR or camera
-   [x] adjust opacity of LCD
-   [x] add image inversion
-   [x] add options to swap between modes
-   [x] laser cut glasses frame

# Extras

-   [x] add some form of app to control settings
-   [x] add options for dimming colour e.g. turn tint red instead of grey tint

# 16/11/2017

connect raspberry pi zero to home WiFi and successfully take photos

# 17/11/2017

successfully connect pi0w to eduroam and take photos

# 18/11/2017

start designing the frame

# 19/11/2017

start work with LCD

-   find c++ library from adafruit [ST7735-c+++](https://github.com/adafruit/Adafruit-ST7735-Library)
-   find python library [ST7735-micro](https://github.com/hosaka/micropython-st7735), [ST7735-af c++ forked to py](https://github.com/cskau/Python_ST7735)

looking thought the code the ST7735-micro seems cleaner and looks like I will be able to modify it easier since it is broken into more small functions although the other python has image support so I will try both and access

# 02/02/2018

start working on project again after exams/coursework and Christmas break but WiFi has stopped working possibly because of certification update but even reslashing the board and rerunning the cat installer didn't work will try to connect when I get home to check the WiFi chip is still working talked to Jake and said he should be able to put it on Plymouth humanoids humanoid5

# 05/02/2018

work on time management and issue tracking

# 06/02/2018

today I finally got the pi0w connected to the uni WiFi and also got the vnc working so that I could work on the pi in uni without brining in a separate screen for the pi once I had done that I started work on the field of view calculations and realised that with out a fisheye camera adapter the lcd has a bigger fov so only the centre will be usable for point adjustment I also calculated the pixels per angle and realise that the only issue with using a fish eye adapter would cause distortion

then followed this [guide](https://www.pyimagesearch.com/2015/12/14/installing-opencv-on-your-raspberry-pi-zero/) to install open cv reach

```bash
pip install numpy
```

before running out of time before space x falcon heavy launch

# 07/02/2018

spacex falcon heavy launch was a success

-   switch to opencv 3.4.0 and finish up install
-   add all dependences to repo

# 08/02/2018

install locked at 84%

# 09/02/2018

get lcd and pi0w header soldered and get pin mappings for each

# 13/02/2018

looking through the code for the lcd drivers again from (19/11/2017) I think the forked adafruit might be better

found skimage and think it will work well with camera

also make new simpler frame prototype ready for laser cutting

# 14/2/2018

had meeting with Phil and he seems happy with progress and direction I'm taking so all good there

# 15/02/2018

got lcd working and even got the lcd to output circles based on x,y,radius,opacity

got blob detection working 'live'

# 16/02/2018

got both lcds working and fine tune timings to work out where the issues are and fine tune the blob detection

# 17/02/2018

tidied files up and got telegram control integrated into shades with control over weather point detection is on or off and the colour / tint level

# 20/02/2018

finalized remote control(4 modes, more colours and toggle-able debug ) and begin optimizing code to try to improve fps f

# 27/02/2018

investigate [capacitve](https://www.rapidonline.com/adafruit-1362-standalone-5-pad-capacitive-touch-sensor-breakout-73-5337) control of system and mount the lenses into the frame and add price list

# 03/03/2018

begin investigating conversion to c/c++ command

```bash
raspistill -o cam.jpg -cfx 128:128 -ifx negative -w 160 -h 128 -rot 270 --thumb none -l
```

```bash
raspistill -t 1000 -tl 0 -o - > img.jpg -cfx 128:128 -ifx negative -w 160 -h 128 -rot 270 --thumb none
```

find [raspicam](http://www.uco.es/investiga/grupos/ava/node/40) cpp api for the camera possible [st7735R](https://github.com/vinodstanur/raspberry-pi-frame-buffer-mapping-to-160x128-ST7735R-LCD) library although might be screen output

[blob](https://github.com/keenerd/quickblob)

achieve 30 fps image stream although the new blob detection might be able to deal with video stream

# 08/03/2018

receive parts and measure current draw at .2/.3 A and start coding for capacitive buttons

# 12/03/2018

finish initial coding for capacitive buttons

# 13/03/2018

fully implement hold for extra functionality

# 14/03/2018

tidy button code and start thinking about mounting

# 16/03/2018

record progress and prep for progress demonstration

# 9/04/2018

implement addwifi so I can add wifi AP's easier using Telegram

# 12/04/2018

tidy debugging prints and improve access error text

# 17/04/2018

redesign the fame for capacitive board and tidy deinitialization of camera

# 20/04/2018

add print to debug toggle, add commenting, add link to access error reply, start making install script to install dependencies

# 22/04/2018

add time to boot and reboot reply to calculate reboot time

# 23/04/2018

tidy code and make pep257 compliant, only update LCD on value change in manual mode

# 24/04/2018

work on report and get new arms cut,fix error #29 ,and add exit functionality so reopen program

# 26/04/2018

do paper work and move telegram API keys to separate file

# 30/04/2018

tidy code by moving jokes, making buttons more dynamic and work on report
