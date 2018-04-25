import smbus #I2C library
import time
import threading

I2C_ADDR = 0x20 #I2C base addres
sbus = smbus.SMBus(1) #enable I2C bus

BTN_MASK = 0b00001000

btn_state = False

btn_listener = null

def setLeds(yellow=False, green=False, red=False):
	ledVals = 0x00
	for idx, colour in enumerate((yellow, green, red)):
		if(colour):
			ledVals = ledVals | (0b1 << idx)

	bus.write_byte(I2C_ADDR, ledVals)

def buttonListener():
    btn_listener = threading.RepeatedTimer(5.0, getButton)

def getButton():
    byte = bus.read_byte(I2C_ADDR)
    btn_state = bool(BTN_MASK & byte))


while True:
    print(btn_state)
    time.sleep(1)

#bus.write_byte( I2C_ADDR, LED_ON ) #set port to 0
#time.sleep(1) #wait 1 sec
#bus.write_byte( I2C_ADDR, LED_OFF ) #set port to 1
#time.sleep(1) 
