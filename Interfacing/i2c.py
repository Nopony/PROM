import smbus #I2C library
import time
import threading
import configparser

c = configparser.ConfigParser('../constants.ini')

bus = smbus.SMBus(1) #enable I2C bus



THRESHOLD_VALUE = (c['ADC']['THRESHOLD_VOLTAGE'] / c['ADC']['MAX_VOLTAGE']) * c['ADC']['MAX_VALUE']

btn_state = False
mic_state = False


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


def checkMic():
	global mic_state

	bus.write_byte(c['I2C']['ADDR_A'], c['ADC']['COMMAND'])
	result = bus.read_word_data(c['I2C']['ADDR_A'], 0x00)
	
	result &= c['ADC']['READ_MASK']
	result = ( (result & c['ADC']['UPPER_BYTE_MASK']) >> 8 ) | ( (result & ~c['ADC']['UPPER_BYTE_MASK']) << 8 )

	if result > c['ADC']['THRESHOLD_VALUE']:
		mic_state = True

	threading.Timer(c['ADC']['POLLING_DELAY'], checkMic).start()
checkMic()

# returns True if mic voltage exceeded threshold since last time getMic was called
def getMic():
	global mic_state
	
	if mic_state:
		mic_state = False
		return True
	return mic_state


while True:
	print(getMic())

	time.sleep(3)
