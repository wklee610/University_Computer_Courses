
# from math import sqrt
# import heapq
import scipy.io as sio
# import matplotlib.pyplot as plt
import numpy as np

from sklearn import datasets, neighbors
# from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

from sklearn.metrics import accuracy_score

import operator
from operator import itemgetter

# For testing
from sklearn.neighbors import RadiusNeighborsClassifier

# load data from mat files

###### ATNT face
Y_train = sio.loadmat(r'C:\Users\Andy\Desktop\csc4008\hw1\ATNT face\trainY.mat')['trainY']
X_train = sio.loadmat(r'C:\Users\Andy\Desktop\csc4008\hw1\ATNT face\trainX.mat')['trainX']
Y_test = sio.loadmat(r'C:\Users\Andy\Desktop\csc4008\hw1\ATNT face\testY.mat')['testY']
X_test = sio.loadmat(r'C:\Users\Andy\Desktop\csc4008\hw1\ATNT face\testX.mat')['testX']

###### Binalpha handwritten
# Y_train = sio.loadmat(r'C:\Users\Andy\Desktop\csc4008\hw1\Binalpha handwritten\trainY.mat')['trainY']
# X_train = sio.loadmat(r'C:\Users\Andy\Desktop\csc4008\hw1\Binalpha handwritten\trainX.mat')['trainX']
# Y_test = sio.loadmat(r'C:\Users\Andy\Desktop\csc4008\hw1\Binalpha handwritten\testY.mat')['testY']
# X_test = sio.loadmat(r'C:\Users\Andy\Desktop\csc4008\hw1\Binalpha handwritten\testX.mat')['testX']

# print(X_train, Y_train)
# print(X_train.shape, Y_train.shape)

x_train = X_train.T     # X_train.shape (644,320)
y_train = Y_train[0]    # Y_train.shape (1, 320)
x_test = X_test.T       # X_test.shape (644, 80)
y_test = Y_test[0]      # Y_test.shape (1, 80)

# print(x_train,y_train)

class DensityClassifier:
    def __init__(self, r=1.0):
        self.radius = r
        self.no_neighbor_in_radius = []

    def fit(self, x_train, y_train):
        self.X_train = x_train
        self.Y_train = y_train

    def predict(self, X_test):
        predictions = []
        for i in range(len(X_test)):
            dist = np.array([euc_dist(X_test[i], x_t) for x_t in self.X_train])
            masked_dist = np.where(dist <= self.radius)[0]
            # print(masked_dist)
            if len(masked_dist) == 0:
                self.no_neighbor_in_radius.append((i, X_test[i]))
                predictions.append(-1)
                continue

            neigh_count = {}
            for idx in masked_dist:
                if self.Y_train[idx] in neigh_count: # check if neighbor's key already in neigh_count
                    neigh_count[self.Y_train[idx]] += 1 # if so, value +1
                else:
                    neigh_count[self.Y_train[idx]] = 1 # else, create a new pair and let its value be 1

            # neigh_count's value is actually the vote count for corresponding key
            # then by default, it will sort a list of tuples by the first element of the tuple
            sorted_neigh_count = sorted(((neigh_count[neigh], neigh) for neigh in neigh_count), reverse=True)
            # print(sorted_neigh_count)
            # and we access the maximum voting item from sorted_neigh_count (sorted_neigh_count[0])
            # and the second item (idx=1) is actually its id (as we do a reverse in sorting)
            predictions.append(sorted_neigh_count[0][1])

        return predictions



def euc_dist(x1, x2):
    return np.sqrt(np.sum((x1-x2)**2))

# the range below is a rough number just for radius reference
# Binalpha
# R > 16: use all label for voting
# R < 5: all points no neighbour
# RVals = np.arange(5,16,1)
# Dataset 1
# R < 200: only 1 test point has neighbors
# R > 950: all points has neighbor

RVals = np.arange(700,800,10)
# accuracies = []
for r in RVals:
  model = DensityClassifier(r)
  model.fit(x_train, y_train)
  pred = model.predict(x_test)
  acc = accuracy_score(y_test, pred)

  # accuracies.append(acc)
  print("---------------------R=", r, "-------------------------")
  print("R = "+str(r)+"; Accuracy: "+str(acc))
  print("No neighbor: ", len(model.no_neighbor_in_radius), "/", len(x_test))

  neigh = RadiusNeighborsClassifier(radius=r, outlier_label='most_frequent')
  neigh.fit(x_train, y_train)
  # print(neigh.classes_)
  # print(type(neigh.classes_))
  # print(len(neigh.classes_))
  pred2 = neigh.predict(x_test)
  acc = accuracy_score(y_test, pred2)
  print("R = "+str(r)+"; Accuracy: "+str(acc))
