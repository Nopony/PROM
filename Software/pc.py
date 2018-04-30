import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

name='name'
os.system("fswebcam " + name + ".jpg")

im = Image.open("name.jpg")
img2arr = np.array(im)
imgplot = plt.imshow(img)
plt.show()
