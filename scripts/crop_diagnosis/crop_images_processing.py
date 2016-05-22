import matplotlib.pyplot as plt
import numpy as np
import skimage.io as io
from skimage.filter import threshold_otsu
from skimage.morphology import erosion, dilation, opening, closing, white_tophat
from skimage.morphology import black_tophat, skeletonize, convex_hull_image
from skimage.morphology import disk
import mysql.connector as connector
import sys

def getPred(r,g,b):
	query = "select * from predicted_values where red="+str(r)+" and green="+str(g)+" and blue=15"+str(b)
	cursor.execute(query)
	nir = cursor.fetchall()
	#nir = np.random.randint(0,255)
	return nir

def computeNDVI(r,g,b,nir):
	index = (nir-r)/(nir+r)
	if index < -0.5:
		color = [241,52,12]
	elif index < 0.5:
		color = [241,206,12]
	elif index < 1:
		color = [67,241,12]
	return color

imagenes = connector.MySQLConnection(user = "root", password = "root", host = "192.168.0.10", database = "imagenes") #192.168.0.10
cursor = imagenes.cursor()

img_gray = io.imread("cliente/IMG_3416.JPG",as_grey=True)
img = io.imread("cliente/IMG_3416.JPG")

thresh = threshold_otsu(img_gray)
binary = img_gray < thresh

selem = disk(6)
binary_opened = closing(binary,selem)

for i in range(binary_opened.shape[0]):
	for j in range(binary_opened.shape[1]):
		if binary_opened[i,j] == True:
			r = img[i,j,0]
			g = img[i,j,1]
			b = img[i,j,2]
			nir = getPred(r,g,b)
			color = computeNDVI(r,g,b,nir)
			img[i,j,0] ,img[i,j,1] ,img[i,j,2]  = color

io.imsave("resultados/img_ind1.jpg",img)

fig = plt.figure(figsize=(12,3.75))
ax1 = plt.subplot(1,4,1,adjustable="box-forced")
ax2 = plt.subplot(1,4,2,sharex=ax1,sharey=ax1,adjustable="box-forced")
ax3 = plt.subplot(1,4,3)
ax4 = plt.subplot(1,4,4,sharex=ax1,sharey=ax1,adjustable="box-forced")

ax1.imshow(img)
ax1.set_title("Original")
ax1.axis("off")

ax2.imshow(img_gray,cmap=plt.cm.gray)
ax2.set_title("BW version")
ax2.axis("off")

ax3.hist(img_gray)
ax3.set_title("Histrograma")
ax3.axvline(thresh, color="r")

ax4.imshow(binary_opened, cmap=plt.cm.gray)
ax4.set_title("Thresholded")
ax4.axis("off")



print binary_opened.shape
print binary_opened.dtype
#print img_gray[100:110,100:110]
#print binary_opened[300:310,300:310]


plt.show()
fig.savefig("resultados/result.jpeg")
