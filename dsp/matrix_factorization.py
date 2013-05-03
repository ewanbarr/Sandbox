#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plot
import matplotlib.cm as cm
from scipy.misc import lena
#Example from
#Singular Value Decomposition Tutorial
#Kirk Baker
#pg 17

#A = np.asarray([[3,1,1],[-1, 3, 1]])
#U,S,VT = np.linalg.svd(A, full_matrices=False)
#S = np.diag(S)
#A_ = np.dot(U, np.dot(S, VT))
#print np.allclose(A, A_)

def lowrank_SVD(input_matrix, approx=50):
    U,S,VT = np.linalg.svd(A, full_matrices=False)
    A_ = np.zeros((len(U), len(VT)))
    e = 0
    for i in xrange(K):
        A_ += S[i]*np.outer(U.T[i],VT[i])
        e += (A[i,:]-A_[i,:])**2
    RMSE = e
    return A_, RMSE

def PMF(input_matrix, approx=50, iterations=30, learning_rate=.001, regularization_rate=.1, randomize=True, print_status=True):
    A = input_matrix
    K = approx
    A = input_matrix
    K = approx
    itr = iterations
    a = learning_rate
    b = regularization_rate
    N = A.shape[0]
    M = A.shape[1]
    U = np.random.randn(N,K)
    V = np.random.randn(K,M)
    if randomize:
        import random
    RMSE=[]
    if print_status:
        print "Starting PMF"
    I = A > 0
    for r in range(itr):
        e = 0
        for i in range(N):
            for j in range(M):
                if I[i,j]:
                    eij = A[i,j] - np.dot(U[i,:],V[:,j])
                    e += eij
                    U[i,:] = U[i,:] + a*(eij*V[:,j] - b*U[i,:])
                    V[:,j] = V[:,j] + a*(eij*U[i,:] - b*V[:,j])
        RMSE.append(e)
        if print_status:
            print "Iteration " + `r` + " RMSE: " + `RMSE[-1]**2`
    A_ = np.dot(U,V)
    return A_,RMSE

def KPMF(input_matrix, approx=50, iterations=30, learning_rate=.001, regularization_rate=.1, randomize=True, print_status=True):
    A = input_matrix
    K = approx
    A = input_matrix
    K = approx
    itr = iterations
    a = learning_rate
    b = regularization_rate
    N = A.shape[0]
    M = A.shape[1]
    U = np.random.randn(N,K)
    V = np.random.randn(K,M)
    if randomize:
        import random
    RMSE=[]
    if print_status:
        print "Starting PMF"
    I = A > 0
    for r in range(itr):
        e = 0
        for i in range(N):
            for j in range(M):
                if I[i,j]:
                    eij = A[i,j] - np.dot(U[i,:],V[:,j])
                    e += eij
                    U[i,:] = U[i,:] + a*(eij*V[:,j] - b*U[i,:])
                    V[:,j] = V[:,j] + a*(eij*U[i,:] - b*V[:,j])
        RMSE.append(e)
        if print_status:
            print "Iteration " + `r` + " RMSE: " + `RMSE[-1]**2`
    A_ = np.dot(U,V)
    return A_,RMSE

#Rework of lena example
#From https://gist.github.com/thearn/5424219
#Full matrix SVD, low rank approximation
approx = K = 50
iterations = I = 10
A = lena()
A_,RMSE=lowrank_SVD(A,approx=K)
plot.figure()
plot.title("Low Rank SVD (full matrix) RMSE = " + `RMSE[-1]`)
plot.imshow(A_, cmap=cm.gray)

#Sparse matrix setup
sparseness = .85
A = lena()
for i in xrange(len(A)):
    for j in xrange(len(A[i])):
        if np.random.rand() < sparseness:
            A[i,j] = 0.

#Sparse lena
plot.figure()
plot.title("Sparse Lena")
plot.imshow(A, cmap=cm.gray)

#Sparse matrix, regular SVD example, low rank approximation
A_,RMSE=lowrank_SVD(A,approx=K)
plot.figure()
plot.title("Low Rank SVD, RMSE = " + `RMSE[-1]`)
plot.imshow(A_, cmap=cm.gray)

#Sparse matrix, gradient descent example
A_,RMSE=PMF(A,approx=K,iterations=I)
plot.figure()
plot.title("PMF, RMSE = " + `RMSE[-1]`)
plot.imshow(A_, cmap=cm.gray)
plot.show()

#Sparse matrix, constrained gradient descent example
A_,RMSE=KPMF(A,approx=K,iterations=I)
plot.figure()
plot.title("Kernelized PMF, RMSE = " + `RMSE[-1]`)
plot.imshow(A_, cmap=cm.gray)
plot.show()
