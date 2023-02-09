
from math import sqrt
import random
import heapq
import numpy as np
from random import random
from turtle import shape
import scipy.io as sio
from sklearn.model_selection import ShuffleSplit

Y_train = sio.loadmat(r'C:\Users\Andy\Desktop\csc4008\hw1\Binalpha handwritten\trainY.mat')
X_train = sio.loadmat(r'C:\Users\Andy\Desktop\csc4008\hw1\Binalpha handwritten\trainX.mat')
Y_test = sio.loadmat(r'C:\Users\Andy\Desktop\csc4008\hw1\Binalpha handwritten\testY.mat')
X_test = sio.loadmat(r'C:\Users\Andy\Desktop\csc4008\hw1\Binalpha handwritten\testX.mat')

import matplotlib.pyplot as plt
plt.switch_backend('agg')

x_train = X_train['trainX']
y_train = Y_train['trainY']
x_test = X_test['testX']
y_test = Y_test['testY']

#x_train_col = x_train.shape[0]
#x_train_row = x_train.shape[1]
#x_test_col = x_test.shape[0]
#x_test_row = x_test.shape[1]

correct_count = 0
error_count = 0

#print(x_train)

###split

x_traint = x_train.T
x_testt = x_test.T
#print(x_traint.shape)
#print(x_traint)
#print(np.vsplit(x_train, 320))
centroids = []

for i in range(26):
    centroid_vector = []
    for h in range(320):
        sum = 0
        for j in range(30*i, 30*(i+1)):
            sum += x_traint[j][h]
        mean = sum/30
        centroid_vector.append(mean)
    #print(len(centroid_vector))
    #np.append(centroids, centroid_vector, axis = 0)
    centroids.append(centroid_vector)
centroid_array = np.array(centroids)

def classification(centroid_array, y_train, x_testt, y_test):
    for row2 in range(26):                  ###iterate for each centroid
        sum = 0
        for col in range(320):
            difference = x_testt[row1][col] - centroid_array[row2][col]
            square = difference**2
            sum += square
        dist = float(sqrt(sum))
        dist_list.append(dist)
    min_dist = min(dist_list)
    index = dist_list.index(min_dist)
    return index+1

predictions = []
for row1 in range(234):                      ###iterate for each test data
    dist_list = []
    actual_label = int(y_test[0][row1])
    prediction = classification(centroid_array, y_train, x_testt, y_test)
    predictions.append(prediction)
    if actual_label == prediction :
        correct_count += 1
    else:
        error_count += 1
print(predictions)

correct_rate = (correct_count/234)*100
error_rate = (error_count/234)*100
print('correct rate is ', correct_rate, '%')
print('error rate is ', error_rate, '%')


