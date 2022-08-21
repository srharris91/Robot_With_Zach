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
GPIO.setup(pin12,GPIO.OUT) # swith left (16) direction
GPIO.setup(pin16,GPIO.OUT) # left motor on or off (backward default)
GPIO.setup(pin20,GPIO.OUT) # swith right (21) direction
GPIO.setup(pin21,GPIO.OUT) # right motor on or off (forward default)
pl = GPIO.PWM(pin16,400)
pr = GPIO.PWM(pin21,400)
pr.start(0)
pl.start(0)

maxdc = 80
STICK_MAX = 65536
TRIGGER_MAX = 1023
CENTER_TOLERANCE=10
print(dir(ecodes))
print(ecodes.ABS_BRAKE)
print(ecodes.ABS_GAS)

axis = {
        ecodes.ABS_X: 'ls_x',
        ecodes.ABS_Y: 'ls_y',
        ecodes.ABS_RX: 'rs_x',
        ecodes.ABS_RY: 'rs_y',
        ecodes.ABS_Z: 'lt',
        ecodes.ABS_RZ: 'rt',
        }
center={
        'ls_x': STICK_MAX/2,
        'ls_y': STICK_MAX/2,
        'rs_x': STICK_MAX/2,
        'rs_y': STICK_MAX/2,
        'lt': 0,
        'rt': 0,
        }
last = {
        'ls_x': STICK_MAX/2,
        'ls_y': STICK_MAX/2,
        'rs_x': STICK_MAX/2,
        'rs_y': STICK_MAX/2,
        'lt': 0,
        'rt': 0,
        }

for event in gamepad.read_loop():
    print(categorize(event))
    print(event.type,ecodes.BTN_A,ecodes.BTN_TR,ecodes.EV_KEY,ecodes.EV_ABS)
    #print(dir(ecodes))
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        if keyevent.keystate == KeyEvent.key_down:
            if keyevent.scancode == ecodes.BTN_A:
                GPIO.output(pin12,GPIO.HIGH) # nothing (switch 16?)
                #GPIO.output(pin16,GPIO.HIGH) # left backwards alone
                pl.ChangeDutyCycle(maxdc) # left
                GPIO.output(pin20,GPIO.LOW) # nothing (switch 21)
                #GPIO.output(pin21,GPIO.HIGH) # right forward alone
                pr.ChangeDutyCycle(maxdc) # right
                print('A Forward')
                #time.sleep(1)
            elif keyevent.scancode == ecodes.BTN_Y:
                GPIO.output(pin12,GPIO.LOW) # nothing (switch 16?)
                #GPIO.output(pin16,GPIO.LOW) # left backwards alone
                pl.ChangeDutyCycle(0) # off
                GPIO.output(pin20,GPIO.LOW) # nothing (switch 21)
                pr.ChangeDutyCycle(0) # off
                #GPIO.output(pin21,GPIO.LOW) # right forward alone
                center['ls_x'] = last['ls_x']
                center['ls_y'] = last['ls_y']
                center['rs_x'] = last['rs_x']
                center['rs_y'] = last['rs_y']
                center['lt'] = last['lt']
                center['rt'] = last['rt']
                print('Y Calibrated')
            elif keyevent.scancode == ecodes.BTN_X:
                GPIO.output(pin12,GPIO.LOW)
                #GPIO.output(pin16,GPIO.LOW)
                pl.ChangeDutyCycle(0) # left
                GPIO.output(pin20,GPIO.LOW)
                #GPIO.output(pin21,GPIO.LOW)
                pr.ChangeDutyCycle(0) # right
                print('X, Breaking')
            elif keyevent.scancode == ecodes.BTN_START:
                GPIO.output(pin12,GPIO.LOW)
                #GPIO.output(pin16,GPIO.LOW)
                pl.ChangeDutyCycle(0) # left
                GPIO.output(pin20,GPIO.LOW)
                #GPIO.output(pin21,GPIO.LOW)
                pr.ChangeDutyCycle(0) # right
                print('Start, Kill')
                break
            elif keyevent.scancode == ecodes.BTN_B:
                GPIO.output(pin12,GPIO.LOW) # nothing (switch 16?)
                #GPIO.output(pin16,GPIO.HIGH) # left backwards alone
                pl.ChangeDutyCycle(maxdc) # left
                GPIO.output(pin20,GPIO.HIGH) # nothing (switch 21)
                #GPIO.output(pin21,GPIO.HIGH) # right forward alone
                pr.ChangeDutyCycle(maxdc) # right
                print('B backward')
                #time.sleep(1)
            elif keyevent.scancode == ecodes.BTN_TR:
                GPIO.output(pin12,GPIO.HIGH) # nothing (switch 16?)
                #GPIO.output(pin16,GPIO.HIGH) # left backwards alone
                pl.ChangeDutyCycle(maxdc) # left
                GPIO.output(pin20,GPIO.HIGH) # nothing (switch 21)
                #GPIO.output(pin21,GPIO.HIGH) # right forward alone
                pr.ChangeDutyCycle(maxdc) # right
                print('TR Right')
                #time.sleep(1)
            elif keyevent.scancode == ecodes.BTN_TL:
                GPIO.output(pin12,GPIO.LOW) # nothing (switch 16?)
                #GPIO.output(pin16,GPIO.HIGH) # left backwards alone
                pl.ChangeDutyCycle(maxdc) # left
                GPIO.output(pin20,GPIO.LOW) # nothing (switch 21)
                #GPIO.output(pin21,GPIO.HIGH) # right forward alone
                pr.ChangeDutyCycle(maxdc) # right
                print('TL Left')
                #time.sleep(1)
        elif keyevent.keystate == KeyEvent.key_up:
            print('let go of button')
            GPIO.output(pin12,GPIO.LOW)
            #GPIO.output(pin16,GPIO.LOW)
            pl.ChangeDutyCycle(0) # left
            GPIO.output(pin20,GPIO.LOW)
            #GPIO.output(pin21,GPIO.LOW)
            pr.ChangeDutyCycle(0) # right
        else: 
            print('unknown event')
    elif event.type == ecodes.EV_ABS:
        keyevent = categorize(event)
        if axis[event.code] in ['ls_x', 'ls_y','rs_x','rs_y','lt','rt']:
            last[axis[event.code]] = event.value

            value = event.value - center[axis[event.code]]

            if abs(value) <= CENTER_TOLERANCE:
                value=0

            if axis[event.code] == 'ls_x':
                if value<0:
                    print('left')
                else:
                    print('right')
                print('value = ',value)
            elif axis[event.code] == 'ls_y':
                if value<0:
                    print('forward')
                else:
                    print('backward')
                print('value = ',value)
            elif axis[event.code] == 'rs_x':
                if value<0:
                    print('Rleft')
                else:
                    print('Rright')
                print('value = ',value)
            elif axis[event.code] == 'rs_y':
                if value<0:
                    print('Rforward')
                else:
                    print('Rbackward')
                print('value = ',value)
            elif axis[event.code] == 'lt':
                if value<0:
                    print('LT negative')
                else:
                    print('LT positive')
                print('value = ',value)
            elif axis[event.code] == 'rt':
                if value<0:
                    print('RT negative')
                else:
                    print('RT positive')
                print('value = ',value)

    else:
        print('did not push ABXY')
        #GPIO.output(pin12,GPIO.LOW)
        #GPIO.output(pin16,GPIO.LOW)
        #GPIO.output(pin20,GPIO.LOW)
        #GPIO.output(pin21,GPIO.LOW)
        #time.sleep(1)
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
pr.stop()
pl.stop()
GPIO.cleanup()
