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

servo_mode = False
SERVO_MODE_MANUAL = False
SERVO_MODE_PID = True
ENABLE_COUNTDOWN = bool(c.get("GENERAL", "ENABLE_COUNTDOWN"))

#setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_SERVO_PWM = int(c.get("GPIO", "SERVO_PWM")) #servo pwm for PID control
GPIO.setup(GPIO_SERVO_PWM, GPIO.OUT)
SERVO_PWM = GPIO.PWM(GPIO_SERVO_PWM, 50)
SERVO_PWM.start(0)

GPIO_SERVO_POWER = int(c.get("GPIO", "SERVO_POWER"))
GPIO.setup(GPIO_SERVO_POWER, GPIO.OUT)

GPIO_BUZZER_PWM = int(c.get("GPIO", "BUZZER_PWM"))
BUZZER_FREQ = int(c.get("GPIO", "BUZZER_FREQUENCY"))
GPIO.setup(GPIO_BUZZER_PWM, GPIO.OUT)
BUZZER_PWM = GPIO.PWM(GPIO_BUZZER_PWM, BUZZER_FREQ)
BUZZER_PWM.start(0)



#setup threads
PID_POLLING_DELAY = float(c.get("PID", "POLLING_DELAY"))


#helper function for servo pins
def setServoControl(mode):
	global servo_mode
	servo_mode = mode

	if servo_mode == SERVO_MODE_MANUAL:
		GPIO.output(GPIO_SERVO_POWER, GPIO.LOW)
	else:
		GPIO.output(GPIO_SERVO_POWER, GPIO.HIGH)
		pidLoop()

	I2C.setLed(I2C.GREEN, mode)
	I2C.setLed(I2C.RED, not mode)



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
	leds.turn(I2C.readMic())

	newThread(0.1, micLedLoop)

def micLoop():
	if I2C.getMic():
		log.append('mic')
		print('Microphone: Cockroach Detected')
	newThread(0.5, micLoop)

def toggleButton():
	pulseBuzzer()
	setServoControl(not servo_mode)

def pulseBuzzer():
	startBuzzer()
	newThread(1, stopBuzzer)

def startBuzzer():
	BUZZER_PWM.ChangeDutyCycle(50)
def stopBuzzer():
	BUZZER_PWM.ChangeDutyCycle(0)
#TODO: Add control loop for transient mic level

if ENABLE_COUNTDOWN:
	I2C.countdown()


#setup button interrupt if in interrupt mode
btn_mode = int(c.get("BTN", "MODE"))
MODE_INT = 3

if btn_mode == MODE_INT:
	I2C.setInterrupt(toggleButton)


#pidLoop()
btnLoop()
#micLoop()


try:

	while True: # main loop
		#image bug detection
		print(threading.active_count())
		I2C.setLed(I2C.YELLOW, True)
		filename = detect.saveImage()
		I2C.setLed(I2C.YELLOW, False)

		bugs = detect.detectBug(filename)
		I2C.setBugCount(bugs)
		if bugs > 0:
			log.append('cam')
			print("[" + log.getTimestamp() + "] Image: Cockroach Detected")
		#TODO: Write bug amount to 7-segment

except KeyboardInterrupt:
	print('Termination signal received, quitting...')
	GPIO.cleanup()
	log.dump()
	print('Cleanup finished')
	quit(0)
