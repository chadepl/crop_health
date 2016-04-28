from skimage.external import tifffile as tif
from skimage import (io, filters, transform)
from skimage import color as color
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as sp

SUMMARY = True
SAVE_NIR = False
SAVE_RGB = False
SAVE_FOR_TRAINING = True
VIEW_NIR = False
VIEW_RGB = False

imNIR = io.imread("../imagenes/vuelo1/nir_sa.tif", plugin = "tifffile")
imNIR = imNIR[:,:,0:3]
imRGB = io.imread("../imagenes/vuelo1/rgb_sa.tif", plugin = "tifffile")
imRGB = imRGB[:,:,0:3]

#Image information

if SUMMARY:

	print "RGB"
	print "--------------------------"
	print "Data type: ", imRGB.dtype
	print "Dimensions: ", imRGB.shape
	print "Elements in the array: ", imRGB.size

	print "***************************"

	print "NIR"
	print "--------------------------"
	print "Data type: ", imNIR.dtype
	print "Dimensions: ", imNIR.shape
	print "Elements in the array: ", imNIR.size

	newNIR = transform.resize(imNIR,imRGB.shape)

	print "***************************"
	print "***************************"

	print "Transformed NIR"
	print "--------------------------"
	print "Data type: ", newNIR.dtype
	#newNIR.dtype = "uint8" # Buggy line: This trasnform multiples by 8 the channels
	print "Changed type: ", newNIR.dtype
	print "Dimensions: ", newNIR.shape
	print "Elements in the array: ", newNIR.size

#Save NIR in text file

if SAVE_NIR:
	f = open("nirinfo.txt","w")
	for x in range(newNIR.shape[0]):
		for y in range(newNIR.shape[1]):
			R = newNIR[x,y,0]
			G = newNIR[x,y,1]
			B = newNIR[x,y,2]
			line = "The point ("+str(x)+","+str(y)+") has RGB equal to: ("+str(R)+","+str(G)+","+str(B)+")"
			if R != 0 and G != 0 and B != 0:
				print line
			f.write(line)
			f.write("\n")

	f.close()
	print "Done with NIR"

#Save RGB in text file

if SAVE_RGB:
	f = open("rgbinfo.txt","w")
	for x in range(imRGB.shape[0]):
		for y in range(imRGB.shape[1]):
			R = imRGB[x,y,0]
			G = imRGB[x,y,1]
			B = imRGB[x,y,2]
			line = "The point ("+str(x)+","+str(y)+") has RGB equal to: ("+str(R)+","+str(G)+","+str(B)+")"
			if R != 0 and G != 0 and B != 0:
				print line
			f.write(line)
			f.write("\n")

	f.close()
	print "Done with RGB"

if SAVE_FOR_TRAINING:
	f = open("training.txt","w")
	for x in range(newNIR.shape[0]):
		for y in range(newNIR.shape[1]):
			R = imRGB[x,y,0]
			G = imRGB[x,y,1]
			B = imRGB[x,y,2]
			Rnir = newNIR[x,y,0]
			line = str(R)+","+str(G)+","+str(B)+","+str(Rnir)
			if R != 0 and G != 0 and B != 0:
				#print line
			f.write(line)
			f.write("\n")

	f.close()
	print "Done saving for training"

if VIEW_NIR:
	io.imshow(imNIR)
	io.show()

if VIEW_RGB:
	io.imshow(imNIR)
	io.show()

print "Done"
