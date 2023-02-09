# Centroid-Classification

Without using below methods  
 - ”sklearn.neighbors.RadiusNeighborsClassifier”  
 - ”sklearn.neighbors.NearestCentroid”  


Centroid method is an agglomerative classification algorithm that uses a centroid to represent a class and make prediction based on the distances between test data point and centroids. Typically, the centroid of each class is found by taking the mean of all data points from the class, and it could be a vector for multi-dimensional dataset. Centroid method is less time-consuming than kNN because it considers centroids or say classes, which are fewer than data vectors. However, since a centroid vector stands for all features in a class, the accuracy of it may be lower.




**Dataset description**

-ATNT FACE DATASET

The file includes training set trainX and their class labels trainY, and test set testX and their class labels testY. Resolution of image is 2823, and 40 classes in total. For each class, there are 8 images for training and 2 images for testing. Each column in trainX and testX represent the 644 pixels of a 2823 image.

-BINALPHA HANDWRITTEN DATASET

The file includes training set trainX and their class labels trainY, and test set testX and their class labels testY. Resolution of image is 2016, and 26 classes in total. For each class, there are 30 images for training and 9 images for testing. Each column in trainX and testX represent the 320 pixels of a 2016 image. When the data is used for testing purpose, the class labels are not needed. But we give them so you can verify the results of your prediction.
