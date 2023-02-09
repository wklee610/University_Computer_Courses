# KNN-Classifier using Euclidean Distance Measurement Method
Write a program to do KNN, run the codes on both the face data and handwritten data.  
It has both version of using KNN-Classifier function and without KNN-Classifier function.

    (i) what is the value of k choose. 
  
    (ii) the predicted class labels for the test images and the percentage errors of test images. 
  
    (iii) other observed results by my code
    
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


**INTRODUCTION**  
I needed to write a program to do KNN and should run the codes on both the face data and handwritten data.  
In the KNN classifier algorithm, storing the training data set is the whole process of creating a model.  
When making predictions on new data points, the algorithm finds the nearest data point, the nearest neighbor, in the training dataset.  
Simply put, can think of it as predicting by finding the closest match in the training dataset.  
The characteristics of this algorithm are instance-based learning (prediction of new data using only each instance), memory-based learning (store all learning data in memory and then try prediction based on it) and lazy learning (It is a lazy algorithm that works only when testing data comes in without training the model separately).  
Various distance measures exist, and the representative method used in this program is the Euclidean distance measurement method.  
The square root of the sum of squares of the difference between the corresponding x and y values, which means the straight-line distance between two observations.
