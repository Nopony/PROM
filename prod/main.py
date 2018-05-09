import i2c as I2C
import detect
import pid as PID
import ConfigParser
import time
import RPi.GPIO as GPIO
import log
import threading


c = ConfigParser.ConfigParser()
c.read('./constants.py')

pid = PID.PID(I2C.getLdr)

#setup operating mode
btn_mode = int(c.get("BTN", "MODE"))
MODE_POLL = 0
MODE_SOFT_DBNC = 1
MODE_SOFT_HARD_DBNC = 2
MODE_INT = 3

servo_mode = False
SERVO_MODE_MANUAL = False
SERVO_MODE_PID = True


#setup GPIO pins
GPIO.setmode(GPIO.BCM)

GPIO_SERVO_PWM = int(c.get("GPIO", "SERVO_PWM")) #servo pwm for PID control
GPIO.setup(GPIO_SERVO_PWM, GPIO.OUT)
SERVO_PWM = GPIO.PWM(GPIO_SERVO_PWM, 50)
SERVO_PWM.start(0)

GPIO_SERVO_POWER = int(c.get("GPIO", "SERVO_POWER"))
GPIO.setup(GPIO_SERVO_POWER, GPIO.OUT)

GPIO_BUTTON_INT = int(c.get("GPIO", "BUTTON_INT"))
GPIO.setup(GPIO_BUTTON_INT, GPIO.IN) #pi pin number here. REMEMBER TO ADD THE PULL UP 10K RESISTOR YOU TWAT
# if btn_mode == MODE_INT:
# 	GPIO.add_event_detect(GPIO_BUTTON_INT, GPIO.FALLING,
#                       callback=eButtonPressed, bouncetime=int(c.get("BTN", "INTERRUPT_DEBOUNCE_PERIOD")))
# 	#TODO: revise unpushed version from userspace, possibly done in I2C module


GPIO_BUZZER_PWM = int(c.get("GPIO", "BUZZER_PWM"))
BUZZER_FREQ = int(c.get("GPIO", "BUZZER_FREQUENCY"))
GPIO.setup(GPIO_BUZZER_PWM, GPIO.OUT)
BUZZER_PWM = GPIO.PWM(GPIO_BUZZER_PWM, BUZZER_FREQ)
BUZZER_PWM.start(0)



#setup threads
PID_POLLING_DELAY = float(c.get("PID", "POLLING_DELAY"))


def pidLoop():
	if servo_mode == SERVO_MODE_MANUAL:
		return
	SERVO_PWM.ChangeDutyCycle(pid.next())
	t = threading.Timer(PID_POLLING_DELAY, pidLoop)
	t.daemon(True)

def btnLoop():
	if I2C.getButton():
		pulseBuzzer()
		setServoControl(not servo_mode)
	t = threading.Timer(0.5, btnLoop)
	t.daemon(True)

def micLoop():
	if I2C.getMic():
		log.append('mic')
		print('Microphone: Cockroach Detected')
	t = threading.Timer(0.5, micLoop)
	t.daemon(True)


def pulseBuzzer():
	startBuzzer()
	t = threading.Timer(1, stopBuzzer)
	t.daemon(True)

def startBuzzer():
	BUZZER_PWM.ChangeDutyCycle(50)
def stopBuzzer():
	BUZZER_PWM.ChangeDutyCycle(0)
#TODO: Add control loop for transient mic level

pidLoop()
btnLoop()
micLoop()

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
try:

	while True: # main loop
		#image bug detection
		I2C.setLed(I2C.YELLOW, True)
		filename = detect.saveImage()
		I2C.setLed(I2C.YELLOW, False)

		bugs = detect.detectBug(filename)
		if bugs > 0:
			log.append('cam')
			print("Image: Cockroach Detected")
		#TODO: Write bug amount to 7-segment

except KeyboardInterrupt:
	print('Termination signal received, quitting...')
	GPIO.cleanup()
	log.dump()
	print('Cleanup finished')
	quit(0)