
#load data
data <- read.csv('../processed_data/horizontal_data.csv')

#RFP DATA
#filter out actin data
rfp.data <- data[!grepl("actin", data$sample_id), ]
#calcualte distances
rfp.distances <- dist(rfp.data)
#get clusters
rfp.clusters <- hclust(rfp.distances)
plot(rfp.clusters)
#assign clusters
rfp.cluster.assignment <- data.frame(cutree(rfp.clusters, h = 1.85))
#save rfp dataframe
rfp.clusts <- rfp.data
rfp.clusts <- cbind(rfp.clusts, rfp.cluster.assignment)
#write to dataframe
write.csv(rfp.clusts, '../processed_data/horizontal_rfp_clusters.csv', row.names=FALSE)

#ACTIN DATA
#get actin data only
actin.data <- data[grepl("actin", data$sample_id), ]
#calcualte distances
actin.distances <- dist(actin.data)
#get clusters 
actin.clusters <- hclust(actin.distances)
plot(actin.clusters)
#assign clusters
actin.cluster.assignment <- data.frame(cutree(actin.clusters, h=1.95))
#save actin data
actin.clusts <- actin.data
actin.clusts <- cbind(actin.clusts, actin.cluster.assignment)
#write to dataframe
write.csv(actin.clusts, '../processed_data/horizontal_actin_clusters.csv', row.names=FALSE)

