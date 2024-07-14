
#load data
data <- read.csv('../processed_data/horizontal_data.csv')

#RFP DATA
#filter out actin data
rfp.data <- data[!grepl("actin", data$sample_id), ]
#calcualte distances
rfp.distances <- dist(rfp.data)
#run PCA
rfp.pca <- prcomp(rfp.distances)
#print summary
print(summary(rfp.pca))

pca.coords <- data.frame(rfp.pca$x)
pca.coords <- cbind(pca.coords, data.frame(rfp.data$sample_id))
write.csv(pca.coords, '../processed_data/horizontal_rfp_pca.csv')

#ACTIN DATA
#filter out actin data
actin.data <- data[grepl("actin", data$sample_id), ]
#calcualte distances
actin.distances <- dist(actin.data)
#run PCA
actin.pca <- prcomp(actin.distances)
#print summary
print(summary(actin.pca))

pca.coords <- data.frame(actin.pca$x)
pca.coords <- cbind(pca.coords, data.frame(actin.data$sample_id))
write.csv(pca.coords, '../processed_data/horizontal_actin_pca.csv')

#total
#calcualte distances
distances <- dist(data)
#run PCA
pca <- prcomp(distances)
#print summary
print(summary(pca))

pca.coords <- data.frame(pca$x)
pca.coords <- cbind(pca.coords, data.frame(data$sample_id))
write.csv(pca.coords, '../processed_data/horizontal_total_pca.csv')




