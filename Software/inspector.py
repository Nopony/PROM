#Just opens the image in MatPlotLib so I can see how good the sample values are
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import sys

if(len(sys.argv) == 2):
    name = sys.argv[1]
else:
    print("Wrong args")
    quit()

image = Image.open(name)
im = np.array(image)

imgplot = plt.imshow(im)
plt.show()
