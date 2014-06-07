#!/usr/bin/env python
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(16, GPIO.IN)
GPIO.setup(18, GPIO.IN)

GPIO.setup(11, GPIO.OUT)
# GPIO.setup(13, GPIO.OUT)
# GPIO.setup(15, GPIO.OUT)
GPIO.output(11, GPIO.LOW)
# GPIO.output(13, GPIO.LOW)
# GPIO.output(15, GPIO.LOW)

# state - decides what LED should be on and off
state = -1

# increment - the direction of states
inc = 1

refresh_time = 0.1

def blink(pin_number, length, rate):
    """
    Function to blink an LED an amount of time at a certain rate.
    """
    total = 0.0
    state = -1

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

    return 0

while True:
    
    if ( GPIO.input(16) == True ):
        blink(11,1.5,0.5);
        blink(11,1,0.25);
        blink(11,1,0.1);

    # # state toggle button is pressed
    # if ( GPIO.input(16) == True ):
    #     if (inc == 1):
    #         state = state + 1;
    #     else:
    #         state = state - 1;

    #     # reached the max state, time to go back (decrement)
    #     if (state == 3):
    #         inc = 0
    #     # reached the min state, go back up (increment)
    #     elif (state == 0):
    #         inc = 1

    #     if (state == 1):
    #         GPIO.output(11, GPIO.HIGH)
    #         # GPIO.output(13, GPIO.LOW)
    #         # GPIO.output(15, GPIO.LOW)
    #     elif (state == 2):
    #         GPIO.output(11, GPIO.HIGH)
    #         # GPIO.output(13, GPIO.HIGH)
    #         # GPIO.output(15, GPIO.LOW)
    #     elif (state == 3):
    #         GPIO.output(11, GPIO.HIGH)
    #         # GPIO.output(13, GPIO.HIGH)
    #         # GPIO.output(15, GPIO.HIGH)
    #     else:
    #         GPIO.output(11, GPIO.LOW)
    #         # GPIO.output(13, GPIO.LOW)
    #         # GPIO.output(15, GPIO.LOW)
    #     print("pressed B1 ", state)

    # # reset button is pressed
    # if ( GPIO.input(18) == True ):
    #     state = 0
    #     inc = 1
    #     GPIO.output(11, GPIO.LOW)
    #     # GPIO.output(13, GPIO.LOW)
    #     # GPIO.output(15, GPIO.LOW)
    #     print("pressed B2 ", state)

    sleep(refresh_time);
