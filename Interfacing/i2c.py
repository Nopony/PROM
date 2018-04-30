import smbus #I2C library
import time
import threading

I2C_B_ADDR = 0x20 #I2C base address
I2C_A_ADDR = 0x21 #built-in I2C with ADC address
bus = smbus.SMBus(1) #enable I2C bus

BTN_MASK = 0b00001000
BTN_POLLING_DELAY = 0.05

ADC_COMMAND = 0b00010000
ADC_READ_MASK = 0b0000111111111111
ADC_UPPER_BYTE_MASK = 0b1111111100000000
ADC_MAX_VALUE = 3852
ADC_THRESHOLD_VOLTAGE = 2.5
ADC_MAX_VOLTAGE = 3
ADC_THRESHOLD_VALUE = (ADC_THRESHOLD_VOLTAGE / ADC_MAX_VOLTAGE) * ADC_MAX_VALUE
ADC_POLLING_DELAY = 0.05

btn_state = False
mic_state = False

def setLeds(yellow=False, green=False, red=False):
	ledVals = 0x00
	for idx, colour in enumerate((yellow, green, red)):
		if(colour):
			ledVals = ledVals | (0b1 << idx)
	bus.write_byte(I2C_B_ADDR, ledVals)
# returns True if button was pressed since the last time getButton was called
def getButton():
	global btn_state
	if(btn_state):
		btn_state = False
		return True
	else:
		return btn_state

def checkButton():
	global btn_state

	byte = bus.read_byte(I2C_B_ADDR)
	masked = BTN_MASK & byte

	if(masked == 0):
		btn_state = True

	threading.Timer(BTN_POLLING_DELAY, checkButton).start()
checkButton()


def checkMic():
	global mic_state

	bus.write_byte(I2C_A_ADDR, ADC_COMMAND)
	result = bus.read_word_data(I2C_A_ADDR, 0x00)
	
	result &= ADC_READ_MASK
	result = ( (result & ADC_UPPER_BYTE_MASK) >> 8 ) | ( (result & ~ADC_UPPER_BYTE_MASK ) << 8 )

	if(result > ADC_THRESHOLD_VALUE):
		mic_state = True

	threading.Timer(ADC_POLLING_DELAY, checkMic).start()
checkMic()

# returns True if mic voltage exceeded threshold since last time getMic was called
def getMic():
	global mic_state
	
	if(mic_state):
		mic_state = False
		return True
	return mic_state


while True:
	print(getMic())

	time.sleep(3)
