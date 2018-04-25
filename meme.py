#PROM
import os
#import Image

name = "name"
os.system("fswebcam "+name+".jpg")
os.system("convert " + name + ".jpg -compress none " +name + ".ppm")
os.system("feh " + name + ".ppm")
