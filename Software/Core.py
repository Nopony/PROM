from PIL import Image
import numpy as np
import bugDetect

#Opening the image
image = Image.open("2buggos.jpg")
im2 = np.array(image)
blobs = []
bugs = bugDetect.detect(im2)
print(bugs)

if not(len(bugs) == 0):
	print(len(bugs),'Bugs Detected')
	for bug in bugs:
		# edit img to have rectangles around it
	#save as a ppm
