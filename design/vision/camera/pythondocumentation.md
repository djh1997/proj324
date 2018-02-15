[docs](https://picamera.readthedocs.io/en/release-1.13/index.html)

- 5MP sensor, 2592x1944 pixels (same as version 1 official Pi camera)
- 1080p video at 30 FPS (or 60 FPS at 720p, 90 FPS at 480p)
- f2.9 lens, 3.60 mm focal length
- 53.50 degrees horizontal, 41.41 degrees vertical field of view (standard and no IR filter versions)
- Approx. dimensions of circuit and camera: 60 x 11.4 x 5.1mm

```bash
sudo apt-get update
sudo apt-get install python3-picamera
```

```python
import picamera
from time import sleep

camera = picamera.PiCamera()

camera.capture('image1.jpg')
sleep(5)
camera.capture('image2.jpg')
```

opencv failed to install and Phil said i would be better off using a simpler program to reduce compute time so am looking at numpy and [skimage](https://github.com/scikit-image/scikit-image)

[b&w image](https://picamera.readthedocs.io/en/release-1.13/api_camera.html?highlight=black%20and%20white#picamera.PiCamera.color_effects)
