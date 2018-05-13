from PIL import Image, ImageDraw
import numpy as np
import datetime
import os
import time

while True:
	start = time.time()
	#Opening an image without libs
	name = "name"
	os.system("fswebcam -r 640x480 -S 4 --no-banner "+name+".ppm")
	#fswebcam -d /dev/video0 -r 640x480 -S 4 --no-banner /home/pi/Animation/$FILENAME

	image = Image.open(name+".ppm")
	im2 = np.array(image)
	end = time.time()
	print(end - start)
