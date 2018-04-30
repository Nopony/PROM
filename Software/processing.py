import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def maxGreen(im):
	recordGreen = 0

	(width, height) = im.shape[0:2]
	print(width,height)
	for x in range(0,width):
	    for y in range(0,height):
	        pixel = im[x-1][y-1]
	        red = pixel[0]
	        green = pixel[1]
	        blue = pixel[2]
	        if(green > recordGreen):
	        	print('boi')
	        	recordGreen = green
	        	print('Vals =', im[x-1][y-1])
	        	im[x-1][y-1] = [255,0,0]
	imgplot = plt.imshow(im)
	plt.show()
	return recordGreen

def detect(im):

	(height,width) = im.shape[0:2]
	print(height,width)
	for x in range(0,width):
	    for y in range(0,height):
	        pixel = im[y][x]
	        red = pixel[0]
	        green = pixel[1]
	        blue = pixel[2]
	        if(green > red and green > blue and green > 200):
	        	print('Pos = ', x, y, 'Vals =', im[y][x])
	        	im[y:][x:] = [244,63,232]
	#im[0:255][0:255] = [0,0,0]
	imgplot = plt.imshow(im)
	plt.show()

	return im



#Opening an image without libs
# name = "name"
# os.system("fswebcam "+name+".jpg")
# os.system("convert " + name + ".jpg -compress none " +name + ".ppm")
# os.system("feh " + name + ".ppm")

#Opening the image
image = Image.open("testimage.jpg")
im = np.array(image)

print(detect(im))


