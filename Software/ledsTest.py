import leds
from random import *
import time

while True:
    x = uniform(0,3)
    print(x,x*2.6)
    leds.turn(x)
    time.sleep(0.5)
