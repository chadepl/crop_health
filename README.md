# Monitoreo de niveles de irrigación y salud vegetal de los cultivos de arroz a partir de imagenes RGB y NIR

El conjunto de scripts presentes en este repositorio 
cumplen la función de medir el índice NDVI para . El trabajo desarrollado no se limitó al dominio de las imágenes sino que también se buscó prescindir de tecnología de captura de imágenes NIR a través de la predicción de estas haciendo uso de algoritmos de machine learning.

El presente es el manual de la aplicación crop_diagnosis para los que deseen hacer uso de ella.

##Contenido 

1. Descripción de la estructura de los directorios.
2. Pre-requisitos para hacer uso del aplicativo.
3. Paso a paso de como correr el código.

## 1.Estructura de los directorios

-scripts  
&nbsp;|--data_setup  
&nbsp;&nbsp;|--lecturaCorrecta
&nbsp;&nbsp;&nbsp;|--image.py
&nbsp;&nbsp;|--modelo_aprendizaje  
&nbsp;&nbsp;&nbsp;|--imagenes.R
&nbsp;|--crop_diagnosis  
&nbsp;&nbsp;|--cliente  
&nbsp;&nbsp;&nbsp;|--IMG_XYZ.JPG  
&nbsp;&nbsp;|--crop_images_processing.py  
&nbsp;&nbsp;|--crop_images_processing_copy.py

## 2.Pre-requisitos

El computador en el que se vaya a correr el código debe tener el siguiguiente software instalado:  
- MySQL v5.6.27   
- R  v0.99896  
- Python v2.7 
 
Adicionalmente, para la fase de entrenamiento del modelo se recomienda un computador con las siguientes especificaciones:  
- Procesador: 3.2GHz
- Memoria: 8Gb

## 3.Paso a paso

Son dos pasos principales para ejecutar el aplicativo: (1) entrenamiento del modelo y (2) cálculo del índice NDVI sobre imágenes del cultivo.

### Entrenamiento del modelo

Esta sección no está pensada para los usuarios finales del aplicativo. Más bien se presenta como una alternativa para las personas que quieran generar su propio modelo predictivo y conectarlo a su propia base de datos.

### Cálculo del índice NDVI

Para esto, en el directorio crop_diagnosis se encuentra el archivo crop_images_processing.py. Este se corre de la siguiente manera:

<code> $ > python crop_images_processing.py [args]</code>

Donde <b>todos</b> los argumentos se deben ingresar y son los siguientes:

* Threshold: -1 si se usa detección automática del umbral(Otsu). De lo contrario un número entre 0 y 1 que indica el umbral manualmente.
* Offset: Positivo o negativo entre 0 y 1 que indica un offset sobre el umbral calculado por Otsu.
* Imagen a analizar: Ruta a la imagen que se quiere analizar.
* Directorio de resultados: Ruta al directorio donde se desea almacenar los resultados.
* Nombre base de imagenes resultado: Prefijo con el que se marcarán todas la imágenes resultado del análisis.

De esta manera, una ejecución ejemplo del código sería:

<code> $ > python crop_images_processing.py -1 0 ~/Desktop/IMG_3416.JPG ~/Desktop/resultados prueba1</code>

Se debe tener en cuenta que la base de datos esta quemada a nivel del software ya que para propositos de esta entrega, la generación de la misma en cualquier máquina no es tarea sencilla ni rápida.
