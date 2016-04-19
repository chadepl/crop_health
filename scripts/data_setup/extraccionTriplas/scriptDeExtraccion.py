from skimage import data, io, filters
from random import randint
import numpy as np
import os
import csv

#with open("resultados/results.csv", "wb") as f:
#
#    writer = csv.writer(f,delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    testImage = np.random.randint(0,255,size = (300,300,3))
#    for i in range(300):
#        for j in range(300):
#            row = testImage[i,j]
#            writer.writerow(row)
#    io.imshow(testImage, cmap="rgb")
#    io.show()








image = data.coins()
edges = filters.sobel(image)
#io.imshow(edges)
#io.show()

randomGrayImage = np.random.randint(0,255,size=(300,300))
#io.imshow(randomGrayImage, cmap="gray")
#io.show()

pathOfProject = os.path.abspath(os.curdir)

imageName = "im_001.png"

fromFile = io.imread(os.path.join(pathOfProject, os.listdir(pathOfProject)[2],imageName), as_gray = False)

io.imshow(fromFile, interpolation="nearest")

io.show()


