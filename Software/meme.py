import pygame
import pygame.camera
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

#Opening an image without libs
# name = "name"
# os.system("fswebcam "+name+".jpg")
# os.system("convert " + name + ".jpg -compress none " +name + ".ppm")
# os.system("feh " + name + ".ppm")

#Taking a picture
pygame.camera.init()
#pygame.camera.list_camera() #Camera detected or not
cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()
for i in range(0,5):
    img = cam.get_image()
img = cam.get_image()
pygame.image.save(img,"filename.jpg")

#Opening the image
im = Image.open("filename.jpg")
img2arr = np.array(im)



imgplot = plt.imshow(im)
plt.show()
