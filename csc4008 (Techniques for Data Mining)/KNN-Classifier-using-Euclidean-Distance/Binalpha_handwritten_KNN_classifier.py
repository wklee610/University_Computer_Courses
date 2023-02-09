
# from math import sqrt
# import heapq
# import matplotlib.pyplot as plt
# from sklearn.model_selection import cross_val_score

import scipy.io as sio
import numpy as np
from sklearn import datasets, neighbors
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import operator
from operator import itemgetter


# load data from mat files

###### ATNT face
# Y_train = sio.loadmat(r'C:\Users\Andy\Desktop\ATNT face\trainY.mat')['trainY']
# X_train = sio.loadmat(r'C:\Users\Andy\Desktop\ATNT face\trainX.mat')['trainX']
# Y_test = sio.loadmat(r'C:\Users\Andy\Desktop\ATNT face\testY.mat')['testY']
# X_test = sio.loadmat(r'C:\Users\Andy\Desktop\ATNT face\testX.mat')['testX']

###### Binalpha handwritten
Y_train = sio.loadmat(r'C:\Users\Andy\Desktop\Binalpha handwritten\trainY.mat')['trainY']
X_train = sio.loadmat(r'C:\Users\Andy\Desktop\Binalpha handwritten\trainX.mat')['trainX']
Y_test = sio.loadmat(r'C:\Users\Andy\Desktop\Binalpha handwritten\testY.mat')['testY']
X_test = sio.loadmat(r'C:\Users\Andy\Desktop\Binalpha handwritten\testX.mat')['testX']



# print(X_train, Y_train)
# print(X_train.shape, Y_train.shape)

x_train = X_train.T     # X_train.shape (644,320)
y_train = Y_train[0]    # Y_train.shape (1, 320)
x_test = X_test.T       # X_test.shape (644, 80)
y_test = Y_test[0]      # Y_test.shape (1, 80)

class KNN:
    def __init__(self, K=3, dist='euc'):
        self.K = K # K accepts an integet
        self.dist = dist # dist accepts 'euc'(lidean) and 'man'(hattan)

    def fit(self, x_train, y_train):
        self.X_train = x_train
        self.Y_train = y_train

    def predict(self, X_test):
        predictions = []
        for i in range(len(X_test)):
            if self.dist == 'euc':
                dist = np.array([euc_dist(X_test[i], x_t) for x_t in self.X_train])
            else:
                print('only support euclidean distance now, try again')
                exit(0);
            # sort the dist arrat and return the index of sorted array
            # get the first k item
            dist_sorted = dist.argsort()[:self.K]
            neigh_count = {}
            for idx in dist_sorted:
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

kVals = np.arange(1,10,1)
accuracies = []
for k in kVals:
  model = KNN(K = k)
  model.fit(x_train, y_train)
  pred = model.predict(x_test)
  acc = accuracy_score(y_test, pred)
  accuracies.append(acc)
  print("K = "+str(k)+"; Accuracy: "+str(acc))



##If we can use knn module...

# # init knn classifier
# knn = neighbors.KNeighborsClassifier()
#
# # try gridsearch on the initialized classifier
# parameters = {'n_neighbors':list(range(1, 10)), 'weights': ['uniform', 'distance'],'metric':['euclidean', 'manhattan']}
#
#
# clf = GridSearchCV(knn, parameters, cv=5, n_jobs=-1)#, scoring='accuracy')
# # by specifying cv=5 here, it automatically use cross validation to check the prams
# results = clf.fit(x_train,y_train)
# print(results.best_score_)
# print(results.best_estimator_)
# print(results.best_params_)
#
# # double test to confirm the best params
# for i in range (1,10):
#     knn = neighbors.KNeighborsClassifier(n_neighbors=i, weights='distance', metric='euclidean')
#     print("k =", i)
#     print("KNN score: %f" % knn.fit(x_train, y_train).score(x_test, y_test))
#
# print("KNN score: %f" % knn.fit(x_train, y_train).score(x_test, y_test))
