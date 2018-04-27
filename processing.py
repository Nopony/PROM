import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

#Opening an image without libs
# name = "name"
# os.system("fswebcam "+name+".jpg")
# os.system("convert " + name + ".jpg -compress none " +name + ".ppm")
# os.system("feh " + name + ".ppm")

#Opening the image
im = Image.open("testimage.jpg")
img2arr = np.array(im)

(width, height) = img2arr.shape[0:2]
print(width,height)
for x in range(width):
    for y in range(height):
        

imgplot = plt.imshow(im)
plt.show()
