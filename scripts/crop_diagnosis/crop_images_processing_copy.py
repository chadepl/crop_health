import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np
import skimage.io as io
from skimage.filter import threshold_otsu
from skimage.morphology import erosion, dilation, opening, closing, white_tophat
from skimage.morphology import black_tophat, skeletonize, convex_hull_image
from skimage.morphology import disk
import mysql.connector as connector
import sys, os

def getPred(r,g,b,dict):
	nir = 0
	try:
		nir = dict[r*255+g*255+b]
	except:
		query = "select * from predicted_values where red="+str(r)+" and green="+str(g)+" and blue="+str(b)
		cursor.execute(query)
		nir = cursor.fetchall()[0][3]
		dict[r*255+g*255+b] = nir
	#nir = np.random.randint(0,255)
	return nir

def computeNDVI(r,g,b,nir):
	index = float(nir-r)/float(nir+r)
	rgb = scalarMap.to_rgba(index)[0:3]
	rgb = [i * 255 for i in rgb]
	return rgb

def computeIndex(r,g,b,nir):
	return float(nir-r)/float(nir+r)

############
#Argumentos#
############

## -1 si se usa Otsu automatico o un valor entre 0 y 1 si se desea establecer manualmente
threshold = float(sys.argv[1])
print threshold

## Offset para el threshold. 0 si no se desea offset(Ideal cuando se usa Otsu y se desea ajustar sobre este)
offset = float(sys.argv[2])
print offset

## Ruta donde se encuentra la imagen a ser procesada
ruta_imagen = sys.argv[3]
print ruta_imagen
if ruta_imagen == "default":
	path_original = "cliente/prueba/IMG_prueba1.JPG"
else:
	path_original = ruta_imagen
if not os.path.exists(path_original): print "No existe el directorio o la imagen"

## Ruta del folder de destino de los resultados
ruta_destino = sys.argv[4]
print ruta_destino
if ruta_destino == "default":
	path_destino = "resultados"
else:
	path_destino = ruta_destino
if not os.path.exists(path_destino): print "No existe el directorio de destino"

## Nombre general de la imagen resultado (prefijo sobre el que se anaden los demas indicadores)
nombre_resultado = sys.argv[5]



fetched_values = {} #New
index_values = []

imagenes = connector.MySQLConnection(user = "root", password = "root", host = "192.168.0.10", database = "imagenes") #192.168.0.10
cursor = imagenes.cursor()

img_gray = io.imread(path_original,as_grey=True)
img = io.imread(path_original)

if threshold == -1:
	thresh = threshold_otsu(img_gray)
else:
	thresh = threshold

binary = img_gray < thresh + offset

selem = disk(6)
binary_opened = closing(binary,selem)

print "Beginning index calculation"

total_size = binary_opened.shape[0] * binary_opened.shape[1] #New
completed_percent = 0 #New
reference_percent = 0 #New
reference_percent_1 = 0 #New

for i in range(binary_opened.shape[0]):
	for j in range(binary_opened.shape[1]):
		if binary_opened[i,j] == True:
			r = img[i,j,0]
			g = img[i,j,1]
			b = img[i,j,2]
			nir = getPred(r,g,b,fetched_values)
			index = computeIndex(r,g,b,nir)
			index_values.append(index)

cNorm = colors.Normalize(vmin=np.percentile(index_values,10), vmax=np.percentile(index_values,90))
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=plt.get_cmap('RdYlGn'))

for i in range(binary_opened.shape[0]):
	for j in range(binary_opened.shape[1]):
		if binary_opened[i,j] == True:
			r = img[i,j,0]
			g = img[i,j,1]
			b = img[i,j,2]
			nir = getPred(r,g,b,fetched_values)
			color_out = computeNDVI(r,g,b,nir)
			img[i,j,0] ,img[i,j,1] ,img[i,j,2]  = color_out

	completed_percent = completed_percent + (binary_opened.shape[1]/float(total_size))*100 #New
	if (completed_percent - reference_percent_1) >=20:
		reference_percent_1 = completed_percent
		io.imsave(os.path.join(path_destino,nombre_resultado+"_"+str(int(round(completed_percent)))+".jpg"),img) #img_ind_prueba1
	if (completed_percent - reference_percent) >=5:
		print str(completed_percent)+"%" #New
		reference_percent = completed_percent

print "Done"

io.imsave(os.path.join(path_destino,nombre_resultado+"_diagnosed.jpg"),img)

#fig = plt.figure(figsize=(12,3.75))
#ax1 = plt.subplot(1,4,1,adjustable="box-forced")
#ax2 = plt.subplot(1,4,2,sharex=ax1,sharey=ax1,adjustable="box-forced")
#ax3 = plt.subplot(1,4,3)
#ax4 = plt.subplot(1,4,4,sharex=ax1,sharey=ax1,adjustable="box-forced")

#ax1.imshow(img)
#ax1.set_title("Original")
#ax1.axis("off")

#ax2.imshow(img_gray,cmap=plt.cm.gray)
#ax2.set_title("BW version")
#ax2.axis("off")

#ax3.hist(img_gray)
#ax3.set_title("Histrograma")
#ax3.axvline(thresh, color="r")

#ax4.imshow(binary_opened, cmap=plt.cm.gray)
#ax4.set_title("Thresholded")
#ax4.axis("off")

# print binary_opened.shape
# print binary_opened.dtype
# #print img_gray[100:110,100:110]
# #print binary_opened[300:310,300:310]


#plt.show()
#fig.savefig("resultados/result.jpeg")
