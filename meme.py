#PROM
import os
from PIL import Image
import numpy as np

name = "name"
os.system("fswebcam "+name+".jpg")
#os.system("convert " + name + ".jpg -compress none " +name + ".ppm")

im = Image.open("name.jpg")
img2arr = np.array(im)
arr2im = Image.fromarray(im2array)
arr2im.save('out.bmp')
