import pygame
import pygame.camera
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

class blob:
    '''A class for the bugs '''
    def __init__(self,x,y):
        self.x = x
        self.y = y

#Returns the square distance
def distS(x1,y1,z1,x2,y2,z2):
	return (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2

#Compares euclidian distance to threshold
def eucdetect(im):
    threshold = 25
    (height,width) = im.shape[0:2]

    for x in range(0,width):
        for y in range(0,height):
            pixel = im[y][x]
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]
            d = distS(red,green,blue,0,255,0)
			#print(d)
			#if(d < threshold * threshold):
            if(d < 52500):
                #print('Pos = ', x, y, 'Vals =', im[y][x]," dist = ",d)
                im[y][x] = [244,63,232]
    imgplot = plt.imshow(im)
    plt.show()

    image = Image.fromarray(im)
    image.save("your_file.jpeg")


#Taking a picture
pygame.camera.init()
#pygame.camera.list_camera() #Camera detected or not
cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()

plt.ion()

while True:
    img = cam.get_image()
    pygame.image.save(img,"filename.jpg")

    #Displaying the image
    im = Image.open("filename.jpg")
    img2arr = np.array(im)

    eucdetect(img2arr)
