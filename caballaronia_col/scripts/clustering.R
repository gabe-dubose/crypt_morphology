
#load data
data <- read.csv('../processed_data/processed_data.csv')

#calcualte distances
distances <- dist(data)
#get clusters
clusters <- hclust(distances)
plot(clusters)
#assign clusters
cluster.assignment <- data.frame(cutree(clusters, h = 2.4))
#save rfp dataframe
clusts <- data
clusts <- cbind(clusts, cluster.assignment)
#write to dataframe
write.csv(clusts, '../processed_data/h2.4_clusters.csv', row.names=FALSE)