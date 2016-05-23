# Nicolás Chaves de Plaza
# Simón Ramírez Amaya
# Crop Health

get_bin_mean <- function(bin_number){
  return(16.5 + (as.numeric(bin_number)-1)*3)
}

# Carga de información desde SQL
conexion = dbConnect(MySQL(), user='root', password='root', dbname='imagenes', host='localhost')
rs = dbSendQuery(imagenes, "select * from training")
data = fetch(rs, n=-1)
# Visualización gráfica del espacio de trabajo
cuts = cut(data$red_nir,breaks = 80)
plot3d(data$red,data$green,data$blue,col=rainbow(80)[cuts],size = 0.01)
# Discretización de red_nir
cuts = cut(data$red_nir,breaks = 80)
data$cuts = as.numeric(cuts)
data$cuts = as.factor(data$cuts)
# Conformación de muestras de entrenamiento y prueba 
set.seed(3464)
sample_size = floor(0.20*nrow(data))
data_sample = data[sample(seq_len(nrow(data)), size = sample_size),]
train_ind = seq_len(floor(nrow(data_sample)*0.5))
train = data_sample[train_ind,]
train$cuts = factor(train$cuts)
test = data_sample[-train_ind,]
test$cuts = factor(test$cuts)
# Entrenamiento
fit <- randomForest(cuts ~ red + green + blue, data=train, xtest=test[,1:3], ytest = test[,5], ntree=50, keep.forest = TRUE)
# Predicción
red <- seq(0,255)
green <- seq(0,255)
blue <-seq(0, 255)
prediction <- expand.grid(red,green,blue)
colnames(prediction) <- c("red","green","blue")
prediction_rf <- predict(fit,prediction)
prediction_rf <- lapply(prediction_rf,get_bin_mean)
prediction_rf <- as.numeric(prediction_rf)
dbWriteTable(conexion, value = prediction[1:1000000,], name = "predicted_values", append = TRUE, row.names = FALSE ) 
dbWriteTable(conexion, value = prediction[1000001:2000000,], name = "predicted_values", append = TRUE, row.names = FALSE ) 
dbWriteTable(conexion, value = prediction[2000001:5000000,], name = "predicted_values", append = TRUE, row.names = FALSE ) 
dbWriteTable(conexion, value = prediction[5000001:10000000,], name = "predicted_values", append = TRUE, row.names = FALSE ) 
dbWriteTable(conexion, value = prediction[10000001:15000000,], name = "predicted_values", append = TRUE, row.names = FALSE ) 
dbWriteTable(conexion, value = prediction[15000001:16777216,], name = "predicted_values", append = TRUE, row.names = FALSE ) 



