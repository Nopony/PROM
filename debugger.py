import pygame
import pygame.camera
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

#Taking a picture
pygame.camera.init()
#pygame.camera.list_camera() #Camera detected or not
cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()

while True:
    img = cam.get_image()
    pygame.image.save(img,"filename.jpg")

    #Displaying the image
    im = Image.open("filename.jpg")
    img2arr = np.array(im)
    imgplot = plt.imshow(im)
    plt.show()
    plt.pause(0.2)

    plt.close('all')
    
