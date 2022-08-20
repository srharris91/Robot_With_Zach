#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
from evdev import InputDevice, categorize, ecodes,KeyEvent

gamepad = InputDevice('/dev/input/event0')

pin12 = 32
pin16 = 36
pin20 = 38
pin21 = 40


GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin12,GPIO.OUT)
GPIO.setup(pin16,GPIO.OUT)
GPIO.setup(pin20,GPIO.OUT)
GPIO.setup(pin21,GPIO.OUT)

for event in gamepad.read_loop():
    print(categorize(event))
    print(event.type,ecodes.BTN_A,ecodes.BTN_TR,ecodes.EV_KEY,ecodes.EV_ABS)
    #print(dir(ecodes))
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        if keyevent.keystate == KeyEvent.key_down:
            if keyevent.scancode == ecodes.BTN_A:
                GPIO.output(pin12,GPIO.HIGH) # nothing (switch 16?)
                GPIO.output(pin16,GPIO.HIGH) # left backwards alone
                GPIO.output(pin20,GPIO.LOW) # nothing (switch 21)
                GPIO.output(pin21,GPIO.HIGH) # right forward alone
                print('A Forward')
                #time.sleep(1)
            elif keyevent.scancode == ecodes.BTN_Y:
                GPIO.output(pin12,GPIO.LOW) # nothing (switch 16?)
                GPIO.output(pin16,GPIO.LOW) # left backwards alone
                GPIO.output(pin20,GPIO.LOW) # nothing (switch 21)
                GPIO.output(pin21,GPIO.LOW) # right forward alone
                print('Y Breaking')
            elif keyevent.scancode == ecodes.BTN_X:
                GPIO.output(pin12,GPIO.LOW)
                GPIO.output(pin16,GPIO.LOW)
                GPIO.output(pin20,GPIO.LOW)
                GPIO.output(pin21,GPIO.LOW)
                print('X, Breaking')
            elif keyevent.scancode == ecodes.BTN_START:
                GPIO.output(pin12,GPIO.LOW)
                GPIO.output(pin16,GPIO.LOW)
                GPIO.output(pin20,GPIO.LOW)
                GPIO.output(pin21,GPIO.LOW)
                print('Start, Kill')
                break
            elif keyevent.scancode == ecodes.BTN_B:
                GPIO.output(pin12,GPIO.LOW) # nothing (switch 16?)
                GPIO.output(pin16,GPIO.HIGH) # left backwards alone
                GPIO.output(pin20,GPIO.HIGH) # nothing (switch 21)
                GPIO.output(pin21,GPIO.HIGH) # right forward alone
                print('B backward')
                #time.sleep(1)
            elif keyevent.scancode == ecodes.BTN_TR:
                GPIO.output(pin12,GPIO.HIGH) # nothing (switch 16?)
                GPIO.output(pin16,GPIO.HIGH) # left backwards alone
                GPIO.output(pin20,GPIO.HIGH) # nothing (switch 21)
                GPIO.output(pin21,GPIO.HIGH) # right forward alone
                print('TR Right')
                #time.sleep(1)
            elif keyevent.scancode == ecodes.BTN_TL:
                GPIO.output(pin12,GPIO.LOW) # nothing (switch 16?)
                GPIO.output(pin16,GPIO.HIGH) # left backwards alone
                GPIO.output(pin20,GPIO.LOW) # nothing (switch 21)
                GPIO.output(pin21,GPIO.HIGH) # right forward alone
                print('TL Right')
                #time.sleep(1)
        elif keyevent.keystate == KeyEvent.key_up:
            print('let go of button')
            GPIO.output(pin12,GPIO.LOW)
            GPIO.output(pin16,GPIO.LOW)
            GPIO.output(pin20,GPIO.LOW)
            GPIO.output(pin21,GPIO.LOW)
        else: 
            print('unknown event')
    else:
        print('did not push ABXY')
        #GPIO.output(pin12,GPIO.LOW)
        #GPIO.output(pin16,GPIO.LOW)
        #GPIO.output(pin20,GPIO.LOW)
        #GPIO.output(pin21,GPIO.LOW)
        time.sleep(1)
    #GPIO.output(pin12,GPIO.LOW)
    #GPIO.output(pin16,GPIO.HIGH)
    #GPIO.output(pin20,GPIO.LOW)
    #GPIO.output(pin21,GPIO.LOW)
    #time.sleep(1)
    #GPIO.output(pin12,GPIO.LOW)
    #GPIO.output(pin16,GPIO.LOW)
    #GPIO.output(pin20,GPIO.HIGH)
    #GPIO.output(pin21,GPIO.LOW)
    #time.sleep(1)
    #GPIO.output(pin12,GPIO.LOW)
    #GPIO.output(pin16,GPIO.LOW)
    #GPIO.output(pin20,GPIO.LOW)
    #GPIO.output(pin21,GPIO.HIGH)
    #print(i)
#
GPIO.cleanup()
