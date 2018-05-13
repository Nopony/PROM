from PIL import Image, ImageDraw
import numpy as np
import pygame
import pygame.camera
import bugDetect
import datetime
import os

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
	im2 = np.array(im)
	bugs = bugDetect.detect(im2)

	if not(len(bugs) == 0):
		print("Image: Cockroach Detected")
		now = datetime.datetime.now()
		print now.strftime("%Y-%m-%d %H:%M")
		draw = ImageDraw.Draw(image)
		for bug in bugs:
			draw.rectangle([bug.minx,bug.miny,bug.maxx,bug.maxy])
		image.save(now.strftime("%Y-%m-%d %H:%M")+".ppm")
