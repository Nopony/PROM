import time
import os
import ConfigParser
import i2c
c = ConfigParser.ConfigParser()
c.read('./constants.ini')

class PID:
    #cb returns momentary sensor value
    def __init__(self, cb):
        """
        Create pid instance. For coefficients see constants.ini
        :param cb: Function returning new values
        :param target: Value to try to maintain
        """
        self.kp = float(c.get('PID', 'KP'))
        self.kd = float(c.get('PID', 'KD'))
        self.ki = float(c.get('PID', 'KI'))
        self.cb = cb
        self.target = float(c.get('PID', 'TARGET_LUMINOSITY'))
        self.prevVal = self.cb()
	self.prevTime = time.time()
	self.maxOutput = float(c.get('PID', 'MAX_OUTPUT'))
	self.minOutput = float(c.get('PID', 'MIN_OUTPUT'))

    def setTarget(self, target):
        """
        Sets new target value
        :param target:
        :return:
        """
        self.target = target
        
    def start(self, initialOutput):
        """
        Initiates PID. Returns no value.

        :return: nothing
        """
        self.prevVal = self.cb()
        self.prevTime = time.time()

	self.output = initialOutput

    def next(self):
        """
        Gets next PID value

        :return: Next value
        """
        t, val = time.time(), self.cb()
        change = \
            self.kp * float(self.target - val) + \
            self.kd * (float(val - self.prevVal) / float(t - self.prevTime)) + \
            self.ki * (float(val - self.prevVal) * float(t - self.prevTime))

	#print("p: " + str((self.target - val)))
	#print("d: " + str((val - self.prevVal) / (t - self.prevTime)))
	#print("i: " + str((val - self.prevVal) * (t - self.prevTime)))
	#print("val: " + str(val))

        self.prevTime = t
        self.prevVal = val
	
	self.output += change
	if self.output < self.minOutput:
		dc = self.minOutput
	elif self.output > self.maxOutput:
		dc = self.maxOutput

        return self.output
