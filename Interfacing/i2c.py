import smbus #I2C library
import time
import threading
import ConfigParser
import RPi.GPIO as GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

c = ConfigParser.ConfigParser()
c.read('./constants.py')
bus = smbus.SMBus(1) #enable I2C bus

I2C_ADDR_A = int(c.get('I2C', 'ADDR_A'), 16)
I2C_ADDR_B = int(c.get('I2C', 'ADDR_B'), 16)

ADC_COMMAND_CH1 = 0b00010000
ADC_COMMAND_CH2 = 0b00100000
ADC_READ_MASK = 0b1111111100001111
ADC_UPPER_BYTE_MASK = 0b1111111100000000
ADC_MAX_VALUE = 4092.0
ADC_MAX_VOLTAGE = 3
ADC_THRESHOLD_VALUE = ADC_MAX_VALUE * (float(c.get('ADC','THRESHOLD_VOLTAGE')) / ADC_MAX_VOLTAGE)
ADC_POLLING_DELAY = float(c.get('ADC', 'POLLING_DELAY'))

BTN_MODE = int(c.get('BTN', 'MODE'), 10)
MODE_POLL = 0
MODE_SOFT_DBNC = 1
MODE_SOFT_HARD_DBNC = 2
MODE_INT = 3


BTN_INT_PIN = int(c.get('GPIO', 'BUTTON_INT'), 10)
BTN_MASK = 0b00000010 if BTN_MODE == 2 else 0b10000000
BTN_POLLING_DELAY = float(c.get('BTN','IDLE_POLLING_DELAY'))
BTN_DEBOUNCE_DELAY = float(c.get('BTN','DEBOUNCE_POLLING_DELAY'))
BTN_DEBOUNCE_STABLE_PERIOD = float(c.get('BTN','DEBOUNCE_STABLE_PERIOD'))

btn_state = False
mic_state = False
btn_cnt = 0
max_btn_cnt = float(c.get('BTN','DEBOUNCE_STABLE_PERIOD')) // float(c.get('BTN','DEBOUNCE_POLLING_DELAY'))
ldr_value = 0

#check if I2C B connected
try:
	bus.write_byte(I2C_ADDR_B, 0)
except IOError:
	raise 'I2C at addr ' + str(I2C_ADDR_B) + ' is not connected.'

#configure I2C expander (I2C B)
bus.write_byte_data(I2C_ADDR_B, 0x03, BTN_MASK) # configuration register 3. Logical 1 is INPUT

def setLeds(yellow=False, green=False, red=False):
	ledVals, regOut = 0x01
	for idx, colour in enumerate((yellow, green, red)):
		if colour
			ledVals = ledVals | (0b1 << (idx + 4))
	bus.write_byte_data(I2C_ADDR_B, regOut, ledVals)


# returns True if button was pressed since the last time getButton was called
def getButton():
	global btn_state
	if btn_state:
		btn_state = False
		return True
	else:
		return btn_state
#just polling, mode 0
def checkButtonNoDebounce():
	global btn_state
	byte = bus.read_byte(I2C_ADDR_B)
	masked = BTN_MASK & byte

	if masked == 0:
		btn_state = True
	threading.Timer(BTN_POLLING_DELAY, checkButtonNoDebounce).start()
#debounce, modes 1 and 2
def checkButton():
	global btn_state, btn_cnt

	byte = bus.read_byte(I2C_ADDR_B)
	masked = BTN_MASK & byte


	if masked == 0 and btn_state == True: # stays on
		threading.Timer(BTN_POLLING_DELAY, checkButton).start()
	elif masked == 0: # False -> True
		if btn_cnt >= max_btn_cnt:
			btn_state = True
			threading.Timer(BTN_POLLING_DELAY, checkButton).start()
		else:
			btn_cnt += 1
			threading.Timer(BTN_DEBOUNCE_DELAY, checkButton).start()
	elif btn_state: # True -> False
		if btn_cnt == 0:
			btn_state = False
			threading.Timer(BTN_POLLING_DELAY, checkButton).start()
		else:
			btn_cnt -= 1
			threading.Timer(BTN_DEBOUNCE_DELAY, checkButton).start()
	else: #stays off
		threading.Timer(BTN_POLLING_DELAY, checkButton).start()


	# if masked == 0:
	#	btn_state = True
	#

#interrupt-based, mode 3
interruptCallback = lambda: print('Unset interrupt callback. This is v. bad.')
def setInterrupt(callback):
	global interruptCallback
	if BTN_MODE != 3:
		print('Interrupt cannot be set in mode ' + str(BTN_MODE))
	interruptCallback = callback
	GPIO.setup(BTN_INT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #pi pin number here. REMEMBER TO ADD THE PULL UP 10K RESISTOR YOU TWAT
	GPIO.add_event_detect(BTN_INT_PIN, GPIO.FALLING, callback=checkInterruptType, bouncetime=1000)
def checkInterruptType():
	if (bus.read_byte(I2C_ADDR_B) & BTN_MASK) == 0 :
		interruptCallback()

if BTN_MODE == 0:
	checkButtonNoDebounce()
elif BTN_MODE == 1 or BTN_MODE == 2:
	checkButton()
else:
	print('Running in mode 3 (interrupt). '
	      'Set the button press-triggered callback with `setInterrupt(cb)`')
#checkButton()


def applyADCMask(raw_result):
	raw_result &= ADC_READ_MASK
	return ((raw_result & ADC_UPPER_BYTE_MASK) >> 8) | ((raw_result & ~ADC_UPPER_BYTE_MASK) << 8)

# reads and converts most recent microphone value
def readMic():
	bus.write_byte(I2C_ADDR_A, ADC_COMMAND_CH1)
	return applyADCMask(bus.read_word_data(I2C_ADDR_A, 0x00))

# reads and converts most recent LDR value
def readLdr():
	bus.write_byte(I2C_ADDR_A, ADC_COMMAND_CH2)
	return applyADCMask(bus.read_word_data(I2C_ADDR_A, 0x00))

# runs in the background and keeps updating ADC
def checkAdc():

	global mic_state, ldr_value

	mic = readMic()
	ldr = readLdr()



	if mic > ADC_THRESHOLD_VALUE:
		mic_state = True
	ldr_value = ldr

	

	threading.Timer(ADC_POLLING_DELAY, checkAdc).start()
checkAdc()

# returns True if mic voltage exceeded threshold since last time getMic was called
def getMic():
	global mic_state
	
	if mic_state:
		mic_state = False
		return True
	return mic_state

def interpolateLdr(val):
	return float(val) / float(ADC_MAX_VALUE) * float(ADC_MAX_VOLTAGE)

# unlike getMic and getButton, this just returns the latest value for the LDR
def getLdr():
	return interpolateLdr(ldr_value) 

print('i2c setup complete')
