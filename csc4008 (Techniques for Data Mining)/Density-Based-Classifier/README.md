# Density-Based-Classifier

**Density Based Classifier**  

Density-based classifier is one way to divide spatial data into different kinds of zones according to data density.  
While many distance-based classifiers can only handle clusters of spherical shape and are sensitive to noise,  
density-based classifier can handle arbitrary-shape clusters and noise point well.  
But it could be time-consuming due to neighborhood search and comparison. 

**Dataset description**  

  -ATNT FACE DATASET  
  
The file includes training set trainX and their class labels trainY, and test set testX and their class
labels testY. Resolution of image is 28*23, and 40 classes in total. For each class, there are 8 images for
training and 2 images for testing. Each column in trainX and testX represent the 644 pixels of a 28*23
image.  
  
  -BINALPHA HANDWRITTEN DATASET  
  
The file includes training set trainX and their class labels trainY, and test set testX and their class
labels testY. Resolution of image is 20*16, and 26 classes in total. For each class, there are 30 images for
training and 9 images for testing. Each column in trainX and testX represent the 320 pixels of a 20*16
image.
When the data is used for testing purpose, the class labels are not needed. But we give them so you can
verify the results of your prediction.
