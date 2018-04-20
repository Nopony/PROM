import smbus #I2C library
import time

I2C_ADDR = 0x20 #I2C base address
bus = smbus.SMBus(1) #enable I2C bus

def setLeds(yellow=False, green=False, red=False):
	ledVals = 0x00
	for idx, colour in enumerate((yellow, green, red)):
		if(colour):
			ledVals = ledVals | (0b1 << idx)

	bus.write_byte(I2C_ADDR, ledVals)

while True:
	setLeds(True, False, False)
	time.sleep(1)
	setLeds(False, True, False)
	time.sleep(1)
	setLeds(False, False, True)
	time.sleep(1)

#bus.write_byte( I2C_ADDR, LED_ON ) #set port to 0
#time.sleep(1) #wait 1 sec
#bus.write_byte( I2C_ADDR, LED_OFF ) #set port to 1
#time.sleep(1) 