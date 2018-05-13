import smbus  # I2C library
import time
import threading
import ConfigParser

c = ConfigParser.ConfigParser()
c.read('./constants.py')
bus = smbus.SMBus(1)  # enable I2C bus

I2C_ADDR_A = int(c.get('I2C', 'ADDR_A'), 16)
I2C_ADDR_B = int(c.get('I2C', 'ADDR_B'), 16)

ADC_COMMAND_CH1 = 0b00010000
ADC_COMMAND_CH2 = 0b00100000
ADC_READ_MASK = 0b1111111100001111
ADC_UPPER_BYTE_MASK = 0b1111111100000000
ADC_MAX_VALUE = 4092.0
ADC_MAX_VOLTAGE = 3
ADC_THRESHOLD_VALUE = ADC_MAX_VALUE * (float(c.get('ADC', 'THRESHOLD_VOLTAGE')) / ADC_MAX_VOLTAGE)
ADC_POLLING_DELAY = float(c.get('ADC', 'POLLING_DELAY'))

BTN_MASK = 0b10000000
BTN_POLLING_DELAY = float(c.get('BTN', 'POLLING_DELAY'))

btn_state = False
mic_state = False
ldr_value = 0


def setInterrupt():
	bus.write_byte_data(I2C_ADDR_B, 0x03, 0b00000001) # configuration register 3. Logical 1 is INPUT
	GPIO.setup(15, GPIO.IN) #pi pin number here. REMEMBER TO ADD THE PULL UP 10K RESISTOR YOU TWAT
	GPIO.add_event_detect(15, GPIO.FALLING, callback=eButtonPressed, bouncetime=300)

def eButtonPressed():
	global btn_state
	print('MAMMA MIA! ITSA BUTTON!')
	btn_state = True

def setLeds(yellow=False, green=False, red=False):
	ledVals = 0x00
	for idx, colour in enumerate((yellow, green, red)):
		if colour:
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


# checkButton()

print('i2c setup complete')

while True:
	print("Waiting for edge")
	GPIO.wait_for_edge(24, GPIO.RISING)
	print("Now that's what I call EDGE")

