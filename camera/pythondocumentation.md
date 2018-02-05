[docs](https://picamera.readthedocs.io/en/release-1.13/index.html)

sudo apt-get update
sudo apt-get install python3-picamera

import picamera
from time import sleep

camera = picamera.PiCamera()

camera.capture('image1.jpg')
sleep(5)
camera.capture('image2.jpg',format='yuv')
