import RPi.GPIO as GPIO

# PIN VALS
leds = [5, 6, 12, 13, 16, 19, 20, 26]

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for led in leds:
	GPIO.setup(led, GPIO.OUT)

def allOff():
	for led in leds:
		GPIO.output(led, GPIO.LOW)


def turn(x, thresholds):
	allOff()

	i = 0
	while x > thresholds[i]:
		GPIO.output(leds[i], GPIO.HIGH)
		i += 1
		if i >= 7:
			break