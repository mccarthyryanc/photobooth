#!/usr/bin/env python
#
# Testing script for the raspicam API
#

import time
import picamera

# with picamera.PiCamera() as camera:
#     camera.resolution = (640, 480)
#     camera.start_preview()
#     camera.start_recording('foo.h264')
#     camera.wait_recording(20)
#     camera.stop_recording()
#     camera.stop_preview()

camera = picamera.PiCamera()
try:
    camera.start_preview()
    time.sleep(10)
    camera.stop_preview()
finally:
    camera.close()