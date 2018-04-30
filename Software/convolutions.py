from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
# x = cv2.imread("lenna.png")
# x = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY) #Convert to black and white

image = Image.open("testimage.jpg")
image = image.convert('L')
im = np.array(image)



kernal = np.array([[-1,-1,-1]
					,[-1,8,-1]
					,[-1,-1,-1]])
emboss = np.array([[-2,-1,0]
					,[-1,1,1]
					,[0,1,2]])
edge = np.array([[0,-1,0]
				,[1,-4,1]
				,[0,1,0]])

output = np.zeros((im.shape[0],im.shape[1]))


def padwithzeros(vector, pad_width, iaxis, kwargs):
     vector[:pad_width[0]] = 0
     vector[-pad_width[1]:] = 0
     return vector

def convolve(image, kernal):
	#Add boarders to the image
	image = np.lib.pad(image,1,padwithzeros)
	print(image)

	for x in range(1,image.shape[0]-1):
		for y in range(1,image.shape[1]-1):
			temp = np.array([[image[x-1][y-1],image[x][y-1],image[x+1][y-1]],
							[image[x-1][y],  image[x][y],  image[x+1][y]],
							[image[x-1][y+1],image[x][y+1],image[x+1][y+1]]])
			output[x-1][y-1] = (np.sum(np.multiply(temp,kernal)))


	oimgplot = plt.imshow(image,cmap='gray')
	plt.show()

	cimgplot = plt.imshow(output, cmap='gray')
	plt.show()

	# cv2.imshow('Original Image',image)
	# cv2.imshow('Filter applied',output)
	# cv2.waitKey(0)                 # Waits forever for user to press any key
	# cv2.destroyAllWindows()        # Closes displayed windows

convolve(im,kernal)
convolve(im,emboss)
convolve(im,edge)
