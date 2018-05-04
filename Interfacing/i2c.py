import smbus #I2C library
import time
import threading
import ConfigParser



c = ConfigParser.ConfigParser()
c.read('./constants.ini')
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

BTN_MASK = 0b10000000
BTN_POLLING_DELAY = float(c.get('BTN','POLLING_DELAY'))

btn_state = False
mic_state = False
ldr_value = 0

def setLeds(yellow=False, green=False, red=False):
	ledVals = 0x00
	for idx, colour in enumerate((yellow, green, red)):
		if(colour):
			ledVals = ledVals | (0b1 << (idx + 4))
	bus.write_byte(I2C_ADDR_B, ledVals)


# returns True if button was pressed since the last time getButton was called
def getButton():
	global btn_state
	if btn_state:
		btn_state = False
		return True
	else:
		return btn_state


def checkButton():
	global btn_state

	byte = bus.read_byte(I2C_ADDR_B)
	masked = BTN_MASK & byte

	if masked == 0:
		btn_state = True

	threading.Timer(BTN_POLLING_DELAY, checkButton).start()
#checkButton()


def applyADCMask(raw_result):
	raw_result &= ADC_READ_MASK
	return ((raw_result & ADC_UPPER_BYTE_MASK) >> 8) | ((raw_result & ~ADC_UPPER_BYTE_MASK) << 8)


def checkAdc():

	global mic_state, ldr_value

	bus.write_byte(I2C_ADDR_A, ADC_COMMAND_CH1)
	mic = applyADCMask(bus.read_word_data(I2C_ADDR_A, 0x00))

	bus.write_byte(I2C_ADDR_A, ADC_COMMAND_CH2)
	ldr = applyADCMask(bus.read_word_data(I2C_ADDR_A, 0x00))

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
"""
while True:
	setLeds(True, False, False)
	print('BTN: ' + str(getButton())
	print('yellow')
	time.sleep(1)
	setLeds(False, True, False)
	print('BTN: ' + str(getButton())
	print('green')
	time.sleep(1)
	setLeds(False, False, False)
	print('BTN: ' + str(getButton())
	print('green')
	time.sleep(1)
	print('BTN: ' + str(getButton())
	print('all')
	setLeds(True, True, True)
	time.sleep(1)
"""
#while True:
#while True:
	#print(getMic())

	#time.sleep(3)
