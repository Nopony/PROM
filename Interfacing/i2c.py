import smbus #I2C library
import time
import threading
import ConfigParser

c = ConfigParser.ConfigParser()
c.read('./constants.ini')
bus = smbus.SMBus(1) #enable I2C bus



THRESHOLD_VALUE = (float(c.get('ADC','THRESHOLD_VOLTAGE')) / float(c.get('ADC','MAX_VOLTAGE'))) * float(c.get('ADC','MAX_VALUE'))

btn_state = False
mic_state = False
ldr_value = None

def setLeds(yellow=False, green=False, red=False):
	ledVals = 0x00
	for idx, colour in enumerate((yellow, green, red)):
		if(colour):
			ledVals = ledVals | (0b1 << idx)
	bus.write_byte(int(c.get('I2C','ADDR_B'), 16), ledVals)


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

	byte = bus.read_byte(int(c.get('I2C', 'ADDR_B'), 16))
	masked = int(c.get('BTN','MASK'), 2) & byte

	if masked == 0:
		btn_state = True

	threading.Timer(float(c.get('BTN','POLLING_DELAY')), checkButton).start()
checkButton()


def applyADCMask(raw_result):
	return (((raw_result & int(c.get('ADC','READ_MASK'), 2)) & int(c.get('ADC','UPPER_BYTE_MASK'), 2)) >> 8) | ((int(c.get('ADC','READ_MASK'), 2) & raw_result & ~int(c.get('ADC','UPPER_BYTE_MASK'), 2)) << 8)


def checkAdc():
	global mic_state, ldr_value

	bus.write_byte(0x21, 0b00010000)
	mic = applyADCMask(bus.read_word_data(0x21, 0x00))

	bus.write_byte(0x21, 0b00100000)
	ldr = applyADCMask(bus.read_word_data(0x21, 0x00))

	print("MIC: " + str(mic))
	print("LDR: " + str(ldr))

	if mic > THRESHOLD_VALUE:
		mic_state = True
	ldr_value = ldr

	threading.Timer(float(c.get('ADC', 'POLLING_DELAY')), checkAdc).start()
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
