from PIL import Image, ImageDraw
import numpy as np
import bugMultiDetectFast
import datetime
import os
import time

#Returns the square distance
def distS3(x1,y1,z1,x2,y2,z2):
	return (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2

bugPos = []

def detect():
    minx = 100000000
    miny = 100000000
    maxx = 0
    maxy = 0
    (height,width) = im2.shape[0:2]
    for x in range(0,width-1):
        for y in range(0,height-1):
            pixel = im2[y][x]
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]
            d = distS3(red,green,blue,8,81,76)
            if(d < 5250):
                im2[y][x] = [0,0,0] #Set it black
                if(x < minx):
    				minx = x
                elif(x > maxx):
                    maxx = x
                if(y < miny):
                    miny = y
                elif(y > maxy):
    				maxy = y
    bugPos.append([minx,miny,maxx,maxy])

image = Image.open("3bugs.jpg")
im2 = np.array(image)
detect()
detect()
print(len(bugPos))
print(bugPos)
