
#load data
data <- read.csv('../processed_data/processed_data.csv')

#calcualte distances
distances <- dist(data)
#run PCA
pca <- prcomp(distances)
#print summary
print(summary(pca))

pca.coords <- data.frame(pca$x)
pca.coords <- cbind(pca.coords, data.frame(data$sample_id))
write.csv(pca.coords, '../processed_data/pca_coordinates.csv')