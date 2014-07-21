#!/usr/bin/env python
#
# Photobooth script
#
import io
import time
import picamera
import RPi.GPIO as GPIO
from datetime import datetime
from subprocess import Popen, PIPE


# GPIO pin constants
led_pin = 17
green_button_pin = 24
red_button_pin = 23

# === PIN Setups ===
GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
# Button setup for "falling edge" detection on press
GPIO.setup(green_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(red_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Led steup
# GPIO.setup(led_pin, GPIO.OUT)
# GPIO.output(led_pin, GPIO.HIGH)

# === General LED Constants ===
# state - decides what LED should be on and off
state = -1
# increment - the direction of states
inc = 1
# refresh time for the GPIO update checks
gpio_refresh_time = 0.1

# === Picture constants ===
max_pic = 4     # Max number of pics
rest_time = 2   # seconds
pic_extn = ".jpg"
filelist = ["image0%d%s"%(num,pic_extn) for num in range(max_pic)]

global print_waiting, external_drive

external_drive = "/media/B64D-7D76"
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
        time.sleep(length)
        #GPIO.output(pin_number, GPIO.HIGH)
        return 0

    # rate is positive, start blinking
    while True:
        state *= -1
        total += rate
        if total > length:
            break

        if (state > 0):
            GPIO.output(pin_number, GPIO.LOW)
            #print "positive state, GPIO.LOW"
        else:
            GPIO.output(pin_number, GPIO.HIGH)
            #print "positive negative, GPIO.HIGH"
        time.sleep(rate)

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
    print datetime.now() , " | Taking picture!"
    with picamera.PiCamera() as camera:
        # camera.resolution = (1440, 900)
        camera.preview_fullscreen = False
        camera.preview_window = (0,0,1440,900)
        camera.start_preview()
        camera.resolution = (450,300)
        for img_file in filelist:
            led_countdown_blink()
            # camera.resolution = (450,300)
            camera.capture(img_file)
            GPIO.output(led_pin, GPIO.HIGH)
            time.sleep(rest_time)
        camera.stop_preview()

def make_photo():
    """
    Function to make the final photo that is saved or printed
    """
    sys_cmd = "montage image00.jpg image01.jpg image02.jpg image03.jpg -tile 2x2 -border 5 -geometry 450x300+0+0 combined_image.png"
    # sys_cmd = "montage image00.jpg image01.jpg -tile 1x2 -border 5 -geometry +0+0 top.jpg && "
    # sys_cmd += "montage image02.jpg image03.jpg -tile 1x2 -border 5 -geometry +0+0 bottom.jpg && "
    # sys_cmd += "montage top.jpg bottom.jpg -tile 2x1 -border 5 -geometry +0+0 combined_image.png"
    # sys_cmd += "convert top_and_bottom.jpg -resize 900x600 combined_image.png"
    
    process = Popen(sys_cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()
    print datetime.now(), " | make_photo out:"
    print out
    print datetime.now(), " | make_photo err:"
    print err

def save_current_image(channel):
    """
    Function callback for the red button. Saves the image
    most recently taken and changes the value of print_waiting
    to exit waiting loop. This is also called after the printing
    an image.
    """
    global print_waiting
    save_cmd = "cp combined_image.png %s/image_%d.png"%(external_drive,int(time.time()))
    print datetime.now(), " | Saving the image: %s"%save_cmd
    
    process = Popen(save_cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()

    print datetime.now(), " | save_image out:"
    print out
    print datetime.now(), " | save_image err:"
    print err
   
    # now finished, stop waiting
    print_waiting = False

def print_current_image(channel):
    """
    Function callback for the green button. Launches
    Subprocess to call print functions and save image
    function.
    """
    global print_waiting

    print_cmd = "lp -d Canon_CP900 combined_image.png"
    print datetime.now(), " | Printing image: %s"%print_cmd

    process = Popen(print_cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()

    print datetime.now(), " | print_photo out:"
    print out
    print datetime.now(), " | print_photo err:"
    print err

    # now finished, stop waiting
    print_waiting = False


if __name__ == '__main__':
     
    # Loop forever
    running = True
    while running:
        try:
            # Led steup
            GPIO.setup(led_pin, GPIO.OUT)
            GPIO.output(led_pin, GPIO.HIGH)

            print datetime.now() , " | Waiting for green putton press..."  
            GPIO.wait_for_edge(green_button_pin, GPIO.RISING)
            # Start the camera and take the pictures
            start_camera()
            make_photo()
            
            # === Start the button listeners for printing/no-printing ===
            GPIO.remove_event_detect(green_button_pin)
            GPIO.setup(green_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(red_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            
            GPIO.add_event_detect(green_button_pin, GPIO.RISING, callback=print_current_image, bouncetime=200)
            GPIO.add_event_detect(red_button_pin, GPIO.FALLING, callback=save_current_image, bouncetime=200)
            timer_start = time.time()
            timer_end = timer_start + 60.0
            
            # Empty loop while waiting for button press
            print_waiting = True
            print datetime.now() , " | Waiting for Green or Red button press..."
            while print_waiting:
                if timer_end < time.time():
                    print datetime.now(), " | Hit timer expiration."
                    save_current_image(-1)
                    print_waiting = False

            # Remove the event listeners so we can start fresh
            GPIO.remove_event_detect(green_button_pin)
            GPIO.remove_event_detect(red_button_pin)
            GPIO.setup(green_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(red_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        except KeyboardInterrupt:
            print datetime.now() , " | Hit ctrl+C, exiting. Good Bye!"
            running = False

    GPIO.cleanup()
