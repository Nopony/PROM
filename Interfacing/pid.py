import time
import os
import ConfigParser
import i2c
c = ConfigParser.ConfigParser()
c.read('./constants.ini')

class PID:
    #cb returns momentary sensor value
    def __init__(self, cb, target):
        """
        Create pid instance. For coefficients see constants.ini
        :param cb: Function returning new values
        :param target: Value to try to maintain
        """
        self.kp = float(c.get('PID', 'KP'))
        self.kd = float(c.get('PID', 'KD'))
        self.ki = float(c.get('PID', 'KI'))
        self.cb = cb
        self.target = target
        self.prev = None

    def setTarget(self, target):
        """
        Sets new target value
        :param target:
        :return:
        """
        self.target = target
        
    def start(self):
        """
        Initiates PID. Returns no value.

        :return: nothing
        """
        self.prevVal = self.cb()
        self.prevTime = time.time()

    def next(self):
        """
        Gets next PID value

        :return: Next value
        """
        t, val = time.time(), self.cb()
        result = \
            self.kp * (self.target - val) + \
            self.kd * ((val - self.prevVal) / (t - self.prevTime)) + \
            self.ki * ((val - self.prevVal) * (t - self.prevTime))

	print("p: " + str((self.target - val)))
	print("d: " + str((val - self.prevVal) / (t - self.prevTime)))
	print("i: " + str((val - self.prevVal) * (t - self.prevTime)))
	print("val: " + str(val))


        self.prevTime = t
        self.prevVal = val

        return result


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

GPIO.setup(10, GPIO.OUT)

p = GPIO.PWM(10, 100)

p.start(0)
p.ChangeDutyCycle(50)

pid = PID(i2c.getLdr, 0.5)
pid.start()
while True:
	time.sleep(0.1)
	val = pid.next()
	print(val)
	p.ChangeDutyCycle(val)
