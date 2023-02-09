import numpy as np
import matplotlib.pyplot as plt

def mds(D,q):
    D = np.asarray(D)
    D_2 = D**2
    Mean = np.mean(D_2)
    Mean_column = np.mean(D_2, axis = 0)
    Mean_row = np.mean(D_2, axis = 1)
    B = np.zeros(D_2.shape)
    for i in range(B.shape[0]):
        for j in range(B.shape[1]):
            B[i][j] = -0.5*(D_2[i][j] - Mean_row[i] - Mean_column[j]+Mean)
    eigVal,eigVec = np.linalg.eig(B)
    X = np.dot(eigVec[:,:q],np.sqrt(np.diag(eigVal[:q])))

    return X

D = [[0,830,906,1171,662,654,567,1296,557,657],
    [830,0,400,350,551,182,481,670,437,1423],
    [906,400,0,608,897,467,352,391,746,1560],
    [1171,350,608,0,752,518,811,679,703,1732],
    [662,551,897,752,0,429,759,1219,168,1040],
    [654,182,467,518,429,0,401,803,286,1241],
    [567,481,352,811,759,401,0,736,590,1225],
    [1296,670,391,679,1219,803,736,0,1088,1950],
    [557,437,746,703,168,286,590,1088,0,1034],
    [657,1423,1560,1732,1040,1241,1225,1950,1034,0]]

label = ['Beijing',
         'Changsha',
         'Chongqing',
         'Guangzhou',
         'Shanghai',
         'Wuhan',
         'Xi_an',
         'Kunming',
         'Nanjing',
         'Harbin']
X = mds(D,2)
plt.plot(X[:,0],X[:,1],'o')
for i in range(X.shape[0]):
    plt.text(X[i,0]+25,X[i,1]-15,label[i])
plt.show()
