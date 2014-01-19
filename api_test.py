#!/usr/bin/env python
#
# Testing script for the raspicam API
#

import io
import time
import picamera
import cv2
import numpy as np

import time
import picamera


max_pic = 4
with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(2)
    count = 0
    for filename in camera.capture_continuous('img{counter:03d}.jpg'):
        if count > max_pic:
            break
        else:
            count += 1
            print('Captured %s' % filename)
            time.sleep(300) # wait 5 minutes

# # Create the in-memory stream
# stream = io.BytesIO()
# with picamera.PiCamera() as camera:
#     camera.start_preview()
#     time.sleep(2)
#     camera.capture(stream, format='jpeg')
# # Construct a numpy array from the stream
# data = np.fromstring(stream.getvalue(), dtype=np.uint8)
# # "Decode" the image from the array, preserving colour
# image = cv2.imdecode(data, 1)
# # OpenCV returns an array with data in BGR order. If you want RGB instead
# # use the following...
# image = image[:, :, ::-1]

# camera = picamera.PiCamera()
# try:
#     camera.start_preview()
#     time.sleep(10)
#     camera.stop_preview()
# finally:
#     camera.close()

# with picamera.PiCamera() as camera:
#     camera.resolution = (640, 480)
#     camera.start_preview()
#     camera.start_recording('foo.h264', inline_headers=False)
#     camera.wait_recording(20)
#     camera.stop_recording()
#     camera.stop_preview()
