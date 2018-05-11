'''
Author: pw897

This module has a detect function that takes in an image and
returns coordinates of rectangles that contain a bug.

'''
import os
from PIL import Image
import numpy as np

#Returns the square distance
def distS3(x1,y1,z1,x2,y2,z2):
	return (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2

def detect(im):
	minx = 100000000
	miny = 100000000
	maxx = 0
	maxy = 0

	(height,width) = im.shape[0:2]
	#print(height,width)
	x = 0
	while(x < width):
		for y in range(0,height,2):
			pixel = im[y][x]
			red = pixel[0]
			green = pixel[1]
			blue = pixel[2]
			d = distS3(red,green,blue,8,81,76)
			#print(d)
			if(d < 5250):
				if(x < minx):
					minx = x
				elif(x > maxx):
					maxx = x
				if(y < miny):
					miny = y
				elif(y > maxy):
					maxy = y
				count = 1
			else:
				count = 10
		x = x + count
	return [minx,miny,maxx,maxy]
