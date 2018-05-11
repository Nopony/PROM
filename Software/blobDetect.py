import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

#Returns the square distance
def distS3(x1,y1,z1,x2,y2,z2):
	return (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2

#Returns the square distance
def distS2(x1,y1,x2,y2):
	return (x2-x1)**2 + (y2-y1)**2

class blob:
	'''A class for the bugs '''
	def __init__(self,x,y):
		self.minx = x
		self.miny = y
		self.maxx = x
		self.maxy = y
	#Draws a rectangle around the image.
	def show():
		##https://stackoverflow.com/questions/37435369/matplotlib-how-to-draw-a-rectangle-on-image
		print('Kms')
	def add(self,x,y):
		self.minx = min(self.minx,x)
		self.miny = min(self.miny,y)

	def isNear(self,x,y):

		cx = max(min(x,maxx),minx)
		cy = max(min(y,maxy),miny)

		d = distS2(cx,cy, x, y)
		if (d < 20**2):
			return True
		else:
			print('Was too big',d)
			return False

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
	        if(red < 50 and blue < 50 and green > 30):
	        	print('Pos = ', x, y, 'Vals =', im[y][x])
	        	im[y][x] = [244,63,232]
	#im[0:255][0:255] = [0,0,0]
	imgplot = plt.imshow(im)
	plt.show()

	return im


#Compares euclidian distance to threshold
def eucdetect(im):
	threshold = 80

	(height,width) = im.shape[0:2]
	print(height,width)
	for x in range(0,width):
		for y in range(0,height):
			pixel = im[y][x]
			red = pixel[0]
			green = pixel[1]
			blue = pixel[2]
			d = distS3(red,green,blue,0,90,40)
						#if(d < 52500):
			if(d < 500):
				#print('Pos = ', x, y, 'Vals =', im[y][x]," dist = ",d)
				#im[y][x] = [244,63,232]

				found = False
				for b in blobs:
					if(b.isNear(x,y)):
						b.add(x,y)
						found = True
						break;


				if(not found):
					r = blob(x,y)
					blobs.append(r)

	#im[0:255][0:255] = [0,0,0]
	#print(blobs)

	# Create figure and axes
	fig,ax = plt.subplots(1)
	imgplot = plt.imshow(im)
	for b in blobs:
		rect = patches.Rectangle((b.minx,b.miny),b.maxx-b.minx,b.maxy-b.miny,linewidth=1,edgecolor='r',facecolor='none')
		ax.add_patch(rect)
	plt.show()

	return im



#Opening an image without libs
# name = "name"
# os.system("fswebcam "+name+".jpg")
# os.system("convert " + name + ".jpg -compress none " +name + ".ppm")
# os.system("feh " + name + ".ppm")

#Opening the image
image = Image.open("betterLight.jpg")
im = np.array(image)

#print(detect(im))
print("I WANT TO DIE")
blobs = []
#print(blobs)

image = Image.open("betterLight.jpg")
im2 = np.array(image)
print(eucdetect(im2))
