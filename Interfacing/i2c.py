import smbus #I2C library
import time
import threading
import configparser

c = configparser.ConfigParser('../constants.ini')

bus = smbus.SMBus(1) #enable I2C bus



THRESHOLD_VALUE = (c['ADC']['THRESHOLD_VOLTAGE'] / c['ADC']['MAX_VOLTAGE']) * c['ADC']['MAX_VALUE']

btn_state = False
mic_state = False
ldr_value = None

def setLeds(yellow=False, green=False, red=False):
	ledVals = 0x00
	for idx, colour in enumerate((yellow, green, red)):
		if(colour):
			ledVals = ledVals | (0b1 << idx)
	bus.write_byte(c['I2C']['ADDR_B'], ledVals)


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

	byte = bus.read_byte(c['I2C']['ADDR_B'])
	masked = c['BTN']['MASK'] & byte

	if masked == 0:
		btn_state = True

	threading.Timer(c['BTN']['POLLING_DELAY'], checkButton).start()
checkButton()


def applyADCMask(raw_result):
	return (((raw_result & c['ADC']['READ_MASK']) & c['ADC']['UPPER_BYTE_MASK']) >> 8) | ((raw_result & ~c['ADC']['UPPER_BYTE_MASK']) << 8)

#TODO: Change ADC command to read Vin1 and Vin2, get both outputs
#TODO: Check if reading 2 bytes twice works or if you need a block read
def checkAdc():
	global mic_state, ldr_value

	bus.write_byte(c['I2C']['ADDR_A'], c['ADC']['COMMAND'])
	mic = applyADCMask(bus.read_word_data(c['I2C']['ADDR_A'], 0x00))
	ldr = applyADCMask(bus.read_word_data(c['I2C']['ADDR_A'], 0x00))


	if mic > c['ADC']['THRESHOLD_VALUE']:
		mic_state = True
	ldr_value = ldr

	threading.Timer(c['ADC']['POLLING_DELAY'], checkAdc).start()
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

while True:
	print(getMic())

	time.sleep(3)
