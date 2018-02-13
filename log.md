# Tasks

- [x] get camera working
- [x] get pi connected over WiFi
- [ ] get LCD connected
- [ ] get raw data from camera for processing
- [ ] get raw brightness from LDR or camera
- [ ] adjust opacity of LCD
- [ ] add image inversion
- [ ] add options to swap between modes
- [ ] laser cut glasses frame

# Extras

- [ ] add some form of app to control settings
- [ ] add options for dimming colour e.g. turn tint red instead of grey tint

# 16/11/2017

connect raspberry pi zero to home WiFi and successfully take photos

# 17/11/2017

successfully connect pi0w to eduroam and take photos

# 18/11/2017

start designing the frame

# 19/11/2017

start work with LCD

- find c++ library from adafruit [ST7735-c+++](https://github.com/adafruit/Adafruit-ST7735-Library)
- find python library [ST7735-micro](https://github.com/hosaka/micropython-st7735), [ST7735-af c++ forked to py](https://github.com/cskau/Python_ST7735)

looking thought the code the ST7735-micro seems cleaner and looks like I will be able to modify it easier since it is broken into more small functions although the other python has image support so I will try both and access

# 02/02/18

start working on project again after exams/coursework and Christmas break but WiFi has stopped working possibly because of certification update but even reslashing the board and rerunning the cat installer didn't work will try to connect when I get home to check the WiFi chip is still working talked to Jake and said he should be able to put it on Plymouth humanoids humanoid5

# 05/02/18

work on time management and issue tracking

# 06/02/18

today I finally got the pi0w connected to the uni WiFi and also got the vnc working so that I could work on the pi in uni without brining in a separate screen for the pi once I had done that I started work on the field of view calculations and realised that with out a fisheye camera adapter the lcd has a bigger fov so only the centre will be usable for point adjustment i also calculated the pixels per angle and realise that the only issue with using a fish eye adapter would cause distortion

then folowed this [guide](https://www.pyimagesearch.com/2015/12/14/installing-opencv-on-your-raspberry-pi-zero/) to install open cv reach

```bash
pip install numpy
```

before running out of time befor space x falcon heavy launch

# 07/02/18

spacex falcon heavy launch was a success

- switch to opencv 3.4.0 and finish up install
- add all dependences to repo

# 08/02/18

install locked at 84%

# 09/02/18

get lcd and pi0w header soldered and get pin mappings for each

# 13/02/18

looking throught the code for the lcd drivers again from (19/11/2017) i think the forked adafruit might be better
