import smbus  # I2C library
import time
import threading
import ConfigParser
import RPi.GPIO as GPIO


c = ConfigParser.ConfigParser()
c.read('./constants.py')
bus = smbus.SMBus(1)  # enable I2C bus

I2C_ADDR_A = int(c.get('I2C', 'ADDR_A'), 16)
I2C_ADDR_B = int(c.get('I2C', 'ADDR_B'), 16)


ADC_ENABLE_PEAK = bool(int(c.get("ADC", "ENABLE_PEAK_DETECTOR")))
ADC_COMMAND_CH1 = 0b00010000 #0b01000000 if ADC_ENABLE_PEAK else
ADC_COMMAND_CH2 = 0b00100000
if ADC_ENABLE_PEAK:
	ADC_COMMAND_CH2 = 0b01000000
ADC_READ_MASK = 0b1111111100001111
ADC_UPPER_BYTE_MASK = 0b1111111100000000
ADC_MAX_VALUE = 4092.0
ADC_MAX_VOLTAGE = 3
ADC_THRESHOLD_VOLTAGE = float(c.get('ADC', 'THRESHOLD_VOLTAGE'))
ADC_THRESHOLD_VALUE = ADC_MAX_VALUE * (ADC_THRESHOLD_VOLTAGE / ADC_MAX_VOLTAGE)
ADC_POLLING_DELAY = float(c.get('ADC', 'POLLING_DELAY'))

BTN_MODE = int(c.get('BTN', 'MODE'))
MODE_POLL = 0
MODE_SOFT_DBNC = 1
MODE_SOFT_HARD_DBNC = 2
MODE_INT = 3

BTN_INT_PIN = int(c.get('GPIO', 'BUTTON_INT'), 10)
BTN_MASK = 0b10000000
if BTN_MODE == MODE_SOFT_HARD_DBNC:
	BTN_MASK = 0b00000001
#print('MASK SET TO: ' + str(BTN_MASK))

BTN_POLLING_DELAY = float(c.get('BTN', 'IDLE_POLLING_DELAY'))
BTN_DEBOUNCE_DELAY = float(c.get('BTN', 'DEBOUNCE_POLLING_DELAY'))
BTN_DEBOUNCE_STABLE_PERIOD = float(c.get('BTN', 'DEBOUNCE_STABLE_PERIOD'))
BTN_DEBOUNCE_WAIT_NEXT_PRESS = float(c.get('BTN', 'DEBOUNCE_WAIT_NEXT_PRESS'))

btn_state = False
mic_state = False
btn_cnt = 0
max_btn_cnt = (BTN_DEBOUNCE_STABLE_PERIOD // BTN_DEBOUNCE_DELAY)
ldr_value = 0
leds = [False, False, False]
sev_seg = 3
sev_seg_enable = False
YELLOW = 0
GREEN = 1
RED = 2

# check if I2C B connected
try:
	bus.write_byte(I2C_ADDR_B, 0)
except IOError:
	raise IOError('I2C at addr ' + str(I2C_ADDR_B) + ' is not connected.')

# configure I2C expander (I2C B)
bus.write_byte_data(I2C_ADDR_B, 0x03, BTN_MASK)  # configuration register 3. Logical 1 is INPUT



def setLed(colour, value):
	global leds
	leds[colour] = value
	updateI2C()

def updateI2C():
	global leds
	ledVals,regOut = 0xFF, 0x01
	#print(leds)
	for idx, colour in enumerate(leds):
		if colour:
			ledVals ^= (0b00000001 << (idx + 4))
	#print("sevseg:")
	#print("{0:b}".format(sev_seg))
	ledVals &= ((0b11110011 | (sev_seg << 2)))
	print(sev_seg_enable)
	if sev_seg_enable:
		ledVals &= 0b11111101
	else:
		ledVals |= 0b00000010
	

	print(" leds: ")
	print("{0:b}".format(ledVals))
	bus.write_byte(I2C_ADDR_B, ledVals)
	#bus.write_byte_data(I2C_ADDR_B, regOut, ledVals) TODO: test further

def countdown():
	global sev_seg_enable, sev_seg
	sev_seg_enable = True
	for i in range(3, -1, -1):
		sev_seg = i
		updateI2C()
		time.sleep(1)

	sev_seg_enable = False
	updateI2C()

def clearBugCount():
	global sev_seg_enable
	sev_seg_enable = False
	updateI2C()

def setBugCount(bugCount):
	global sev_seg, sev_seg_enable
	
	sev_seg_enable = True
	sev_seg = max(min(bugCount, 3), 0)
	
	updateI2C()
	threading.Timer(1, clearBugCount).start()
	


# returns True if button was pressed since the last time getButton was called
def getButton():
	global btn_state, btn_cnt
	if btn_state:
		btn_state = False
		btn_cnt = 0
		return True
	else:
		return btn_state



# just polling, mode 0
def checkButtonNoDebounce():
	global btn_state
	byte = bus.read_byte(I2C_ADDR_B)
	masked = BTN_MASK & byte
	form ="{0:b}".format(masked)
	form = '0' * (8 - len(form)) + form
	#print(form)

	if masked == 0:
		btn_state = True
	threading.Timer(BTN_POLLING_DELAY, checkButtonNoDebounce).start()


# debounce, modes 1 and 2
def checkButton():
	global btn_state, btn_cnt

	byte = bus.read_byte(I2C_ADDR_B)
	
	
	masked = BTN_MASK & byte
	form ="{0:b}".format(masked)
	form = '0' * (8 - len(form)) + form
	#print(form)
	
	
	#print(btn_cnt)
	if masked == 0 and btn_state == True:  # stays on
		threading.Timer(BTN_DEBOUNCE_WAIT_NEXT_PRESS, checkButton).start()
	elif masked == 0:  # False -> True
		#print("I2C read:" + form)
		if btn_cnt >= max_btn_cnt:
			btn_state = True
			threading.Timer(BTN_DEBOUNCE_WAIT_NEXT_PRESS, checkButton).start()
		else:
			btn_cnt += 1
			threading.Timer(BTN_DEBOUNCE_DELAY, checkButton).start()
	elif btn_state:  # True -> False
		if btn_cnt == 0:
			#btn_state = False
			threading.Timer(BTN_POLLING_DELAY, checkButton).start()
		else:
			btn_cnt -= 1
			threading.Timer(BTN_DEBOUNCE_DELAY, checkButton).start()
	else:  # stays off
		btn_cnt = 0
		threading.Timer(BTN_POLLING_DELAY, checkButton).start()




# interrupt-based, mode 3

def unsetInterrupt():
	raise Exception('Unset interrupt callback in mode 3. This is v. v. bad.')
interruptCallback = unsetInterrupt

def setInterrupt(callback):
	global interruptCallback
	if BTN_MODE != 3:
		print('Interrupt cannot be set in mode ' + str(BTN_MODE))
	interruptCallback = callback
	GPIO.setup(BTN_INT_PIN, GPIO.IN,
	           pull_up_down=GPIO.PUD_UP)  # pi pin number here. REMEMBER TO ADD THE PULL UP 10K RESISTOR YOU TWAT
	GPIO.add_event_detect(BTN_INT_PIN, GPIO.FALLING, callback=checkInterruptType, bouncetime=1000)


def checkInterruptType(e):
	if (bus.read_byte(I2C_ADDR_B) & BTN_MASK) == 0:
		interruptCallback()


if BTN_MODE == 0:
	checkButtonNoDebounce()
elif BTN_MODE == 1 or BTN_MODE == 2:
	checkButton()
else:
	print('Running in mode 3 (interrupt). '
	      'Set the button press-triggered callback with `setInterrupt(cb)`')


# checkButton()
def interpolateVoltage(val):
	return float(val) / float(ADC_MAX_VALUE) * float(ADC_MAX_VOLTAGE)

def applyADCMask(raw_result):
	raw_result &= ADC_READ_MASK
	return ((raw_result & ADC_UPPER_BYTE_MASK) >> 8) | ((raw_result & ~ADC_UPPER_BYTE_MASK) << 8)

# reads and converts most recent microphone value
def readMic():
	bus.write_byte(I2C_ADDR_A, ADC_COMMAND_CH1)
	return interpolateVoltage(applyADCMask(bus.read_word_data(I2C_ADDR_A, 0x00)))


# reads and converts most recent LDR value
def readLdr():
	bus.write_byte(I2C_ADDR_A, ADC_COMMAND_CH2)
	return interpolateVoltage(applyADCMask(bus.read_word_data(I2C_ADDR_A, 0x00)))


# runs in the background and keeps updating ADC
def checkAdc():
	global mic_state, ldr_value

	mic = readMic()
	ldr = readLdr()
	
	#print('LDR: ' + str(ldr) + ' | MIC: ' + str(mic))


	if mic > 1.7:
		print(mic)

	if mic > ADC_THRESHOLD_VOLTAGE:
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





# unlike getMic and getButton, this just returns the latest value for the LDR
def getLdr():
	return ldr_value
