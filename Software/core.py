from PIL import Image, ImageDraw
import numpy as np
import bugDetect
import datetime
import os

while True:
	#Opening an image without libs
	name = "name"
	#os.system("fswebcam -r 640x480 --no-banner "+name+".jpg") #160x120
	os.system("fswebcam -r 176x144 -S 4 --no-banner "+name+".ppm")
	#fswebcam -d /dev/video0 -r 640x480 -S 4 --no-banner /home/pi/Animation/$FILENAME

	#Opening the image
	image = Image.open(name+".ppm")
	im2 = np.array(image)
	blobs = []
	bugs = bugDetect.detect(im2)

	if not(len(bugs) == 0):
		print(len(bugs),'Bugs Detected')
		print("Image: Cockroach Detected")
		now = datetime.datetime.now()
		print now.strftime("%Y-%m-%d %H:%M")
		draw = ImageDraw.Draw(image)
		for bug in bugs:
			draw.rectangle([bug.minx,bug.miny,bug.maxx,bug.maxy],fill=None,outline=(255,0,0))
		image.save(now.strftime("%Y-%m-%d %H:%M")+".ppm")
