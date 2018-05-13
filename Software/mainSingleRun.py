from PIL import Image, ImageDraw
import numpy as np
import bugDetectFast
import datetime
import os
import time

start = time.time()

image = Image.open("betterLight.jpg")
im2 = np.array(image)
blobs = []
bugPos = bugDetectFast.detect(im2)
print(bugPos)

if not(bugPos == [100000000,100000000,0,0]):
	print("Image: Cockroach Detected")
	now = datetime.datetime.now()
	print now.strftime("%Y-%m-%d %H:%M")
	draw = ImageDraw.Draw(image)
	draw.rectangle(bugPos)
	image.save(now.strftime("%Y-%m-%d %H:%M")+".ppm")
else:
	print("No bugs")

end = time.time()
print("Time in secs = " + str(end - start))
