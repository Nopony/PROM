from PIL import Image, ImageDraw
import numpy as np
import bugDetectFast
import datetime
import os

def saveImage(device='/dev/video0', filename='name.jpg'):
	#Opening an image without libs
	#os.system("fswebcam -r 640x480 --no-banner "+name+".jpg") #160x120
	os.system("fswebcam -r 288x352 -S 4 --no-banner -d " + device + " " + filename)
	return filename
	#fswebcam -d /dev/video0 -r 640x480 -S 4 --no-banner /home/pi/Animation/$FILENAME

def detectBug(filename):
	image = Image.open(filename)
	im2 = np.array(image)
	blobs = []
	bugPos = bugDetectFast.detect(im2)
	#print(bugPos)

	if not(bugPos == [100000000,100000000,0,0]):
	#	print("Image: Cockroach Detected")
		now = datetime.datetime.now()
	#	print(now.strftime("%Y-%m-%d %H:%M"))

		draw = ImageDraw.Draw(image)
		draw.rectangle(bugPos)
		image.save(now.strftime("%Y-%m-%d %H:%M")+".ppm")
		return 1
	else:
		return 0
