from skimage.external import tifffile as tif
from skimage import io, filters
import numpy as np
import matplotlib.pyplot as plt

imNIR = io.imread("nir_sa.tif")
#imRGB = tif.imread("rgb_sa.tif")

newImg = threshold_adaptive(imNIR,15)

##print "Data type: ",type(im)
#print "Shape: "
#print im.shape()
#print "Size: "
#print im.size()
#for index,(x,y,z), value in np.ndenumerate(im):
#    print "Index"+str(index)+str(x)+str(y)+str(x)+" Value: "+str(value)
#tif.imshow(imNIR)
#tif.imshow(imRGB)

io.imshow(newImg)

io.show()
