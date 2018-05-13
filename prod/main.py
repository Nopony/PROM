import i2c as I2C
import detect
import pid as PID
import ConfigParser
import time
import RPi.GPIO as GPIO
import log
import threading
import leds


c = ConfigParser.ConfigParser()
c.read('./constants.py')

pid = PID.PID(I2C.getLdr)

#setup operating mode

servo_mode = True
SERVO_MODE_MANUAL = False
SERVO_MODE_PID = True
ENABLE_COUNTDOWN = bool(int(c.get("GENERAL", "ENABLE_COUNTDOWN")))
if ENABLE_COUNTDOWN:
	I2C.countdown()

ENABLE_MULTIPLE_BUGS = bool(int(c.get("GENERAL", "MULTIPLE_BUGS")))




#setup GPIO pins
GPIO.setmode(GPIO.BCM)

GPIO_SERVO_PWM = int(c.get("GPIO", "SERVO_PWM")) #servo pwm for PID control
print("pwm on pin: " + str(GPIO_SERVO_PWM))
GPIO.setup(GPIO_SERVO_PWM, GPIO.OUT)
SERVO_PWM = GPIO.PWM(GPIO_SERVO_PWM, 50)
SERVO_PWM.start(0)
SERVO_PWM.ChangeDutyCycle(5)

GPIO_SERVO_POWER = int(c.get("GPIO", "SERVO_POWER"))
GPIO.setup(GPIO_SERVO_POWER, GPIO.OUT)
GPIO.output(GPIO_SERVO_POWER, GPIO.HIGH)

GPIO_BUZZER_PWM = int(c.get("GPIO", "BUZZER_PWM"))
BUZZER_FREQ = int(c.get("GPIO", "BUZZER_FREQUENCY"))
GPIO.setup(GPIO_BUZZER_PWM, GPIO.OUT)
BUZZER_PWM = GPIO.PWM(GPIO_BUZZER_PWM, BUZZER_FREQ)


#setup LED thresholds
led_thresholds = list(map(lambda t: float(c.get(*t)), [('LED', 'T' + str(i)) for i in range(8)]))


#setup threads
PID_POLLING_DELAY = float(c.get("PID", "POLLING_DELAY"))


#helper function for servo pins
def updateServoControl():
	
	if servo_mode == SERVO_MODE_MANUAL:
		GPIO.output(GPIO_SERVO_POWER, GPIO.LOW)
	else:
		GPIO.output(GPIO_SERVO_POWER, GPIO.HIGH)
		pidLoop()

	I2C.setLed(I2C.GREEN, servo_mode)
	I2C.setLed(I2C.RED, not servo_mode)



def newThread(delay, fun):
	t = threading.Timer(delay, fun)
	t.setDaemon(True)
	t.start()

def pidLoop():
	if servo_mode == SERVO_MODE_MANUAL:
		return
	SERVO_PWM.ChangeDutyCycle(pid.next())

	newThread(PID_POLLING_DELAY, pidLoop)

def btnLoop():
	if I2C.getButton():
		print('Button pressed!')
		toggleButton()

	newThread(0.5, btnLoop)

def micLedLoop():
	leds.turn(I2C.readMic(), led_thresholds)
	newThread(0.01, micLedLoop)

def micLoop():
	if I2C.getMic():
		log.append('mic')
		print('[' + log.getTimestamp() + '] Microphone: Cockroach Detected')
	
	newThread(0.5, micLoop)

def toggleButton():
	global servo_mode
	servo_mode = not servo_mode
	updateServoControl()
	pulseBuzzer()


def pulseBuzzer():
	global SERVO_PWM

	BUZZER_PWM.start(0)

	startBuzzer()
	newThread(1, stopBuzzer)


def startBuzzer():
	#print('STARTING BUZZ')
	BUZZER_PWM.ChangeDutyCycle(50)
def stopBuzzer():
	#print('STOPPING BUZZ')
	BUZZER_PWM.ChangeDutyCycle(0)
	SERVO_PWM.start(0)
	SERVO_PWM.ChangeDutyCycle(pid.next())

	




#setup button interrupt if in interrupt mode
btn_mode = int(c.get("BTN", "MODE"))
MODE_INT = 3

print(btn_mode)


I2C.setLed(I2C.GREEN, True) # default mode is automatic

#setup the threads
if btn_mode == MODE_INT:
	print('Enabling button interrupt')
	I2C.setInterrupt(toggleButton)
else:
	print('Enabling button looping')

	btnLoop()

pidLoop()
micLoop()
micLedLoop()

try:

	while True: # main loop
		#image bug detection
		#print("threads: " + str(threading.active_count()))
		I2C.setLed(I2C.YELLOW, True)
		filename = detect.saveImage()
		I2C.setLed(I2C.YELLOW, False)
		bugs = 0
		if ENABLE_MULTIPLE_BUGS:
			bugs = detect.detectMultiple(filename)
		else:
			bugs = detect.detectBug(filename)
		I2C.setBugCount(bugs)
		if bugs > 0:
			log.append('cam')
			print("[" + log.getTimestamp() + "] Image: Cockroach Detected")
			if ENABLE_MULTIPLE_BUGS:
				print('Number of bugs: ' + str(bugs))

except KeyboardInterrupt:
	print('Termination signal received, quitting...')
	GPIO.cleanup()
	log.dump()
	print('Cleanup finished')
	quit(0)
