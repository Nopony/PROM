import i2c
import time
while True:
	time.sleep(0.2)
	print('LDR: '+ str(i2c.getLdr()))
 

