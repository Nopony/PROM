from PIL import Image, ImageDraw
import numpy as np
import bugDetectFast
import bugMultiDetect
import datetime
import subprocess

def saveImage(device='/dev/video0', filename='name.ppm'):
	#Opening an image without libs
	#os.system("fswebcam -r 640x480 --no-banner "+name+".jpg") #160x120
	subprocess.check_output("fswebcam -r 176x144 -S 4 --no-banner -q -d " + device + " " + filename, shell=True)

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
		draw.rectangle(bugPos,outline=(255,0,0))
		image.save(now.strftime("%Y-%m-%d %H:%M")+".ppm")
		return 1
	else:
		return 0

def multiBug(filename):
	image = Image.open(filename)
	im2 = np.array(image)
	blobs = []
	bugs = bugMultiDetect.detect(im2)

	if(len(bugs) > 3):
		return 3

	if not(len(bugs) == 0):
		# print(len(bugs),'Bugs Detected')
		# print("Image: Cockroach Detected")
		now = datetime.datetime.now()
		# print now.strftime("%Y-%m-%d %H:%M")
		draw = ImageDraw.Draw(image)
		for bug in bugs:multi
			draw.rectangle([bug.minx,bug.miny,bug.maxx,bug.maxy],fill=None,outline=(255,0,0))
		image.save(now.strftime("%Y-%m-%d %H:%M")+".ppm")
	return len(bugs)
