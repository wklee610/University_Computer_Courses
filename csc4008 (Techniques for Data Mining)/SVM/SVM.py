from calendar import c
import numpy as np

import matplotlib.pyplot as plt

from sklearn import svm

from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

X, Y = make_blobs(n_samples=200, centers=2, random_state=6, center_box=(-1,1))

ax = plt.gca()
plt.scatter(X[:,0],X[:,1],c=Y,s=50)
#plt.scatter(X[Y==1, 0], X[Y==1, 1], c='r',marker='o')
#plt.scatter(X[Y==0, 0], X[Y==0, 1], c='b',marker='s')

xlim = ax.get_xlim()
ylim = ax.get_ylim()
axisx = np.linspace(xlim[0],xlim[1],30)
axisy = np.linspace(ylim[0],ylim[1],30)
xx,yy = np.meshgrid(axisx,axisy)

xy = np.vstack([xx.ravel(), yy.ravel()]).T

plt.scatter(xy[:,0],xy[:,1],s=1)

X_train,X_test,y_train,y_test = train_test_split(X,Y,test_size=0.2)
parameters = {
    'gamma': np.linspace(0.0001, 1),
    'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
}
model = svm.SVC()
grid_model = GridSearchCV(model, parameters, cv=10, return_train_score=True)
grid_model.fit(X_train,y_train)

pred_label = grid_model.predict(X_test)
print('accuracy: ', accuracy_score(pred_label, y_test))

print(grid_model.best_params_)
#clf = svm.SVC(kernel='rbf', C=0.1, gamma=grid_model.best_params_['gamma']).fit(X_train,y_train)
clf = svm.SVC(kernel=grid_model.best_params_['kernel'], C=0.01).fit(X_train,y_train)
#clf = svm.SVC(kernel='linear', C=0.1).fit(X,Y)
#clf.fit(X, Y)

Z = clf._decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
#plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, -1], c='r', marker='o')
#X_1 = xx[(yy==1)&(Z<0)]
#X_2 = xx[(yy==0)&(Z>0)]
#X_3 = xx[((yy==1)&(Z>=0))|((yy==0)&(Z<=0))]
#print(X_1.shape)

#plt.scatter(X_1[:,0], X_1[:,1], c='r',marker='o')
#plt.scatter(X_2[:,0], X_2[:,1], c='b',marker='s')
#plt.scatter(X_3[:,0], X_3[:,1], c='g')

ax.contour(xx,yy,Z
	,colors="r"
	,levels=3 
	,alpha=0.5
	,linestyles=["-","-","-"])
ax.set_xlim(xlim)
ax.set_ylim(ylim)

plt.show()



