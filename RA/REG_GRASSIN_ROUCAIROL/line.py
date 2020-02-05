#!/usr/local/bin/python

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


class Line:
    def __init__(self, batch_size):
        self.nb_dims = 1
        self.theta = np.zeros(shape=(batch_size, self.nb_dims+1))

    def f(self, x):
        """
        Get the FA output for a given input variable(s)

        :param x: A single or vector of dependent variables with size [Ns] for which to calculate the features

        :returns: the function approximator output
        """
        if np.size(x) == 1:
            xl = np.vstack(([x], [1]))
        else:
            xl = np.vstack((x, np.ones((1, np.size(x)))))
        return np.dot(self.theta, xl)

    # ----------------------#
    # # Training Algorithm ##
    # ----------------------#

    def train_ls(self, x_data, y_data):
        # Finds the Least Square optimal weights

        XT = []
        
        for x in x_data:
            
            tmp = (x,1)
            
            XT.append(tmp)
            
        X = np.array(XT)

        #X = np.array(x_data)
        #X = np.stack((X,np.ones(X.shape)))
        Y = np.array(y_data)
        Y = np.reshape(Y,(Y.size,1))
 
        self.theta = np.dot(np.dot(np.linalg.inv(np.dot(X.T,X)),X.T),Y).T[0]
        slope = self.theta[0]
        intercept = self.theta[1]
        r_value = np.corrcoef(x_data,y_data)[0][1]
        print(slope)
        print(intercept)
        print(r_value)
        print("theta:", self.theta)

        # ----------------------#
        # # Training Algorithm ##
        # ----------------------#

    def train_regularized(self, x_data, y_data, coef):
        # Finds the regularized Least Square optimal weights

        I = np.identity(2)

        XT = []
        
        for x in x_data:
            
            tmp = (x,1)
            
            XT.append(tmp)
            
        X = np.array(XT)

        #X = np.array(x_data)
        #X = np.stack((X,np.ones(X.shape)))
        Y = np.array(y_data)
        Y = np.reshape(Y,(Y.size,1))
 
        self.theta = np.dot(np.dot(np.linalg.inv(coef*I+np.dot(X.T,X)),X.T),Y).T[0]
        print("theta regularized:", self.theta)

    # ----------------------#
    # # Training Algorithm ##
    # ----------------------#

    def train_from_stats(self, x_data, y_data):
        # Finds the Least Square optimal weights: python provided version
        slope, intercept, r_value, _, _ = stats.linregress(x_data, y_data)

        print(slope)
        print(intercept)
        print(r_value)

        self.theta = [slope, intercept]
        print("theta from stats:", self.theta)

    # -----------------#
    # # Plot function ##
    # -----------------#

    def plot(self, x_data, y_data):
        xs = np.linspace(0.0, 1.0, 1000)
        z = self.f(xs)

        plt.plot(x_data, y_data, 'o', markersize=3, color='lightgreen')
        plt.plot(xs, z, lw=2, color='red')
        plt.show()
