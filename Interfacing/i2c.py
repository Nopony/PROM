import smbus #I2C library
import time
import threading

I2C_B_ADDR = 0x20 #I2C base address
I2C_A_ADDR = 0x21 #built-in I2C with ADC address
bus = smbus.SMBus(1) #enable I2C bus

BTN_MASK = 0b00001000
BTN_POLLING_DELAY = 0.05

ADC_COMMAND = 0b00010000

btn_state = False
mic_state = False

def setLeds(yellow=False, green=False, red=False):
	ledVals = 0x00
	for idx, colour in enumerate((yellow, green, red)):
		if(colour):
			ledVals = ledVals | (0b1 << idx)
	bus.write_byte(I2C_B_ADDR, ledVals)

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

#checkButton()


def checkMic():
	global mic_state

	bus.write_byte(I2C_A_ADDR, ADC_COMMAND)
	result = bus.read_byte(I2C_A_ADDR)

	print(result)



while True:
	checkMic()
	time.sleep(0.02)

#bus.write_byte( I2C_B_ADDR, LED_ON ) #set port to 0
#time.sleep(1) #wait 1 sec
#bus.write_byte( I2C_B_ADDR, LED_OFF ) #set port to 1
#time.sleep(1) 
