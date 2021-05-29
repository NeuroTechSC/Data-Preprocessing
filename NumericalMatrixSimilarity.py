import numpy as np
from scipy.spatial.distance import pdist, squareform

def dcov(X, Y):
    n = X.shape[0]
    XY = np.multiply(X, Y)
    cov = np.sqrt(XY.sum()) / n
    return cov

def dvar(X):
    return np.sqrt(np.sum(X ** 2 / X.shape[0] ** 2))

def cent_dist(X):
    M = squareform(pdist(X))
    rmean = M.mean(axis=1)
    cmean = M.mean(axis=0)
    gmean = rmean.mean()
    R = np.tile(rmean, (M.shape[0], 1)).transpose()
    C = np.tile(cmean, (M.shape[1], 1))
    G = np.tile(gmean, M.shape)
    CM = M - R - C + G
    return CM

def dcor(X, Y):
    assert X.shape[0] == Y.shape[0]

    A = cent_dist(X)
    B = cent_dist(Y)

    dcov_AB = dcov(A, B)
    dvar_A = dvar(A)
    dvar_B = dvar(B)

    dcor = 0.0
    if dvar_A > 0.0 and dvar_B > 0.0:
        dcor = dcov_AB / np.sqrt(dvar_A * dvar_B)

    return dcor

X = np.array([[0, 1, 2, 3, 4],
              [5, 6, 7, 8, 9],
              [10, 11, 12, 13, 14]])

Y = np.array([[0, 1, 2.1, 3, 4],
              [5, 6, 7.1, 8, 9],
              [10, 11.1, 12, 13, 14]])

Z = np.array([[0, 1, 4, 2.1, 3, 4, 3],
              [5, 6.1, 5, 7, 8.1, 9, 6],
              [10, 11, 12, 7, 13.1, 14, 9]])

print(dcor(X, Z))