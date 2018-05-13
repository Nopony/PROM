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

while True:
    print "LED on"
    GPIO.output(led0,GPIO.HIGH)
    GPIO.output(led1,GPIO.HIGH)
    GPIO.output(led2,GPIO.HIGH)
    GPIO.output(led3,GPIO.HIGH)
    GPIO.output(led4,GPIO.HIGH)
    GPIO.output(led5,GPIO.HIGH)
    GPIO.output(led6,GPIO.HIGH)
    GPIO.output(led7,GPIO.HIGH)
    time.sleep(1)
    print "LED off"
    GPIO.output(led0,GPIO.LOW)
    GPIO.output(led1,GPIO.LOW)
    GPIO.output(led2,GPIO.LOW)
    GPIO.output(led3,GPIO.LOW)
    GPIO.output(led4,GPIO.LOW)
    GPIO.output(led5,GPIO.LOW)
    GPIO.output(led6,GPIO.LOW)
    GPIO.output(led7,GPIO.LOW)
    time.sleep(1)
