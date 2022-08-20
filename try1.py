#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

pin12 = 32
pin16 = 36
pin20 = 38
pin21 = 40


GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin12,GPIO.OUT)
GPIO.setup(pin16,GPIO.OUT)
GPIO.setup(pin20,GPIO.OUT)
GPIO.setup(pin21,GPIO.OUT)

for i in range(10):
    GPIO.output(pin12,GPIO.HIGH)
    GPIO.output(pin16,GPIO.LOW)
    GPIO.output(pin20,GPIO.LOW)
    GPIO.output(pin21,GPIO.LOW)
    time.sleep(1)
    GPIO.output(pin12,GPIO.LOW)
    GPIO.output(pin16,GPIO.HIGH)
    GPIO.output(pin20,GPIO.LOW)
    GPIO.output(pin21,GPIO.LOW)
    time.sleep(1)
    GPIO.output(pin12,GPIO.LOW)
    GPIO.output(pin16,GPIO.LOW)
    GPIO.output(pin20,GPIO.HIGH)
    GPIO.output(pin21,GPIO.LOW)
    time.sleep(1)
    GPIO.output(pin12,GPIO.LOW)
    GPIO.output(pin16,GPIO.LOW)
    GPIO.output(pin20,GPIO.LOW)
    GPIO.output(pin21,GPIO.HIGH)
    print(i)

GPIO.cleanup()
