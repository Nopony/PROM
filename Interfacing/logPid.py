import RPi.GPIO as GPIO
import pid as PID
import i2c
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(10, GPIO.OUT)

p = GPIO.PWM(10, 50)

p.start(0)


pid = PID.PID(i2c.getLdr)
pid.start(5)

dc = 1
p.ChangeDutyCycle(5)
while True:
	time.sleep(0.1)
	#print("change: " + str(val) + " current: " + str(dc))
	p.ChangeDutyCycle(pid.next())
