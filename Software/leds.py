import RPi.GPIO as GPIO
import time
# while True:
#     print(i2c.readMic())

#PIN VALS
led0 = 5
led1 = 6
led2 = 12
led3 = 13
led4 = 16
led5 = 19
led6 = 20
led7 = 26

#GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led0,GPIO.OUT)
GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)
GPIO.setup(led3,GPIO.OUT)
GPIO.setup(led4,GPIO.OUT)
GPIO.setup(led5,GPIO.OUT)
GPIO.setup(led6,GPIO.OUT)
GPIO.setup(led7,GPIO.OUT)

def allOff():
    GPIO.output(led0,GPIO.LOW)
    GPIO.output(led1,GPIO.LOW)
    GPIO.output(led2,GPIO.LOW)
    GPIO.output(led3,GPIO.LOW)
    GPIO.output(led4,GPIO.LOW)
    GPIO.output(led5,GPIO.LOW)
    GPIO.output(led6,GPIO.LOW)
    GPIO.output(led7,GPIO.LOW)

def turn(x):
    level = x * 2.6
    # print(level)
    allOff()
    if (level > 0):
            GPIO.output(led0,GPIO.HIGH)
    if (level > 1):
            GPIO.output(led1,GPIO.HIGH)
    if (level > 2):
            GPIO.output(led2,GPIO.HIGH)
    if (level > 3):
            GPIO.output(led3,GPIO.HIGH)
    if (level > 4):
            GPIO.output(led4,GPIO.HIGH)
    if (level > 5):
            GPIO.output(led5,GPIO.HIGH)
    if (level > 6):
            GPIO.output(led6,GPIO.HIGH)
    if (level > 7):
            GPIO.output(led7,GPIO.HIGH)
