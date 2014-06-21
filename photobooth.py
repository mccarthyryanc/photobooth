#!/usr/bin/env python
#
# Photobooth script
#
import io
import time
import picamera
import RPi.GPIO as GPIO
from datetime import datetime

# GPIO pin constants
led_pin = 11
green_button_pin = 16
red_button_pin = 18

# === PIN Setups ===
# GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
# Button setup for "falling edge" detection on press
GPIO.setup(green_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(red_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Led steup
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, GPIO.HIGH)

# === General LED Constants ===
# state - decides what LED should be on and off
state = -1
# increment - the direction of states
inc = 1
# refresh time for the GPIO update checks
gpio_refresh_time = 0.1

# === Picture constants ===
max_pic = 4     # Max number of pics
cam_rest_time = 3   # seconds
pic_extn = ".jpg"
filelist = ["image0%d"%num for num in range(max_pic)]
print_waiting = True


# === LED Functions ===
def blink(pin_number, length, rate):
    """
    Function to blink an LED an amount of time at a certain rate.
    """
    total = 0.0
    state = -1

    # If rate is negative, just leave led on
    # for amount of length
    if rate < 0:
        GPIO.output(pin_number, GPIO.LOW)
        sleep(length)
        GPIO.output(pin_number, GPIO.HIGH)
        return 0

    # rate is positive, start blinking
    while True:
        state *= -1
        total += rate
        if total > length:
            break

        if (state > 0):
            GPIO.output(pin_number, GPIO.LOW)
            print "positive state, GPIO.LOW"
        else:
            GPIO.output(pin_number, GPIO.HIGH)
            print "positive negative, GPIO.HIGH"
        sleep(rate)

    return 0

def led_countdown_blink():
    """
    Function to blink the led more rapidly
    before taking a picture.
    """
    blink(led_pin,2.0,0.5);
    blink(led_pin,2.0,0.25);
    blink(led_pin,2.0,0.1);
    blink(led_pin,1.0,-1);

# === Picture Functions ===
def start_camera():
    """
    Function to start the camera preview and take
    the pictures
    """
    print datetime.now() , " Taking picture!"
    with picamera.PiCamera() as camera:
        camera.resolution = (1800, 1200)
        camera.start_preview()
        for img_file in filelist:
            led_countdown_blink()
            camera.capture(img_file)
            time.sleep(rest_time)
        camera.stop_preview()

def save_current_image():
    """
    Function callback for the red button. Saves the image
    most recently taken and changes the value of print_waiting
    to exit waiting loop. This is also called after the printing
    an image.
    """
    global print_waiting


    # now finished, stop waiting
    print_waiting = False

def print_current_image():
    """
    Function callback for the green button. Launches
    Subprocess to call print functions and save image
    function.
    """
    


if __name__ == '__main__':
     
    # Loop forever
    running = True
    while running:
        try:
            print datetime.now() , " | Waiting for green putton press..."  
            GPIO.wait_for_edge(green_button_pin, GPIO.FALLING)
            # === Start the button listeners for printing/no-printing ===
            GPIO.add_event_detect(green_button_pin, GPIO.FALLING, callback=print_current_image, bouncetime=300)
            GPIO.add_event_detect(red_button_pin, GPIO.FALLING, callback=save_current_image, bouncetime=300)

            # Start the camera and take pictures
            start_camera()
            # Empty loop while waiting for 
            print_waiting = True
            print datetime.now() , " | Waiting for Green or Red button press..."
            while print_waiting:
                continue



        except KeyboardInterrupt:
            print datetime.now() , "Hit ctrl+C, exiting. Good Bye!"
            running = False

    GPIO.cleanup()