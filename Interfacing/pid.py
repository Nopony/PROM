import time

class PID:
    #cb returns momentary sensor value
    def __init__(self, cb, target, kp, ki, kd):
        """
        Create pid instance. For coefficients see constants.ini
        :param cb: Function returning new values
        :param target: Value to try to maintain
        :param kp: proportional coefficient
        :param ki: integral coefficient
        :param kd: derivative coefficient
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.cb = cb
        self.target = target
        self.prev = None


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
        self.prevVal = \
            self.kp * (self.target - val) + \
            self.kd * ((val - self.prevVal) / (t - self.prevTime)) + \
            self.ki * ((val - self.prevVal) * (t - self.prevTime))


pid = PID()