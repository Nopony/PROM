from PIL import Image, ImageDraw
import numpy as np
import bugDetect
import datetime
import os

while True:
	#Opening an image without libs
	name = "name"
	os.system("fswebcam "+name+".jpg")
	os.system("convert " + name + ".jpg -compress none " +name + ".ppm")

	image = Image.open(name+".ppm")
	im2 = np.array(image)
	blobs = []
	bugs = bugDetect.detect(im2)

	if not(len(bugs) == 0):
		print("Image: Cockroach Detected")
		now = datetime.datetime.now()
		print now.strftime("%Y-%m-%d %H:%M")
		draw = ImageDraw.Draw(image)
		for bug in bugs:
			draw.rectangle([bug.minx,bug.miny,bug.maxx,bug.maxy])
		image.save(now.strftime("%Y-%m-%d %H:%M")+".ppm")
