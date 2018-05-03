import time
import os
import ConfigParser
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

        self.prevTime = t
        self.prevVal = val

        return result