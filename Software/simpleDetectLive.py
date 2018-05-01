import os
import pygame
import pygame.camera
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
		self.maxx = max(self.maxx, x)
		self.maxy = max(self.maxy, y)

	def isNear(self,x,y):
		cx = (self.minx + self.maxx)/2
		cy = (self.miny + self.minx)/2
		d = distS2(cx,cy, x, y)
		if (d < 250**2):
			return True
		else:
			#print('Was too big',d)
			return False

	def __str__(self):
		return 'Blob at position ('+str(self.minx) +', '+ str(self.miny) +', '+ str(self.maxx) +', '+  str(self.maxy) +') '


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
	        	#print('Pos = ', x, y, 'Vals =', im[y][x])
				#im[y][x] = [244,63,232]
				found = False
				for b in blobs:
					if(b.isNear(x,y)):
						b.add(x,y)
						found = True
						break;
				if(not found):
					newBlob = blob(x,y)
					blobs.append(newBlob)
				if not(len(blobs)== 1):
					print("Its got",len(blobs),"blobs m8")
					for b in blobs:
						print(b)
					#imgplot = plt.imshow(im)
					#plt.show()
					#quit()
	# Create figure and axes
	fig,ax = plt.subplots(1)
	imgplot = plt.imshow(im)
	for b in blobs:
		print(b.minx,b.miny,b.maxx,b.maxy)
		rect = patches.Rectangle((b.minx,b.miny),b.maxx-b.minx,b.maxy-b.miny,linewidth=1,edgecolor='r',facecolor='none')
		ax.add_patch(rect)
	plt.show()


#Opening the image
image = Image.open("betterLight.jpg")
im2 = np.array(image)

#Taking a picture
pygame.camera.init()
#pygame.camera.list_camera() #Camera detected or not
cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()

plt.ion()

while True:
	blobs = []
	img = cam.get_image()
	pygame.image.save(img,"filename.jpg")
    #Displaying the image
	im = Image.open("filename.jpg")
	img2arr = np.array(im)
	detect(img2arr)
	plt.pause(0.2)
	plt.close('all')
