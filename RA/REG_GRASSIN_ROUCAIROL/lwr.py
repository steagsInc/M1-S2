import numpy as np
import matplotlib.pyplot as plt
from gaussians import Gaussians


def weight(x):
    """
    Get the output of the features for a given input variable(s)

    :param x: a single or vector of dependent variables with size [Ns] for which to calculate the Fa features

    :returns: a vector of feature outputs with size [NumFeats x Ns]
    """
    if np.size(x) == 1:
        w = np.vstack(([x], [1]))

    else:
        w = np.vstack((x, np.ones((1, np.size(x)))))
    return w


class LWR(Gaussians):
    def __init__(self, nb_features):
        super().__init__(nb_features)
        self.theta = np.zeros((2, self.nb_features))

    def f(self, x):
        """
        Get the FA output for a given input variable(s)

        :param x: a single or vector of dependent variables with size [Ns] for which to calculate the FA features

        :returns: a vector of function approximator outputs with size [Ns]
        """
        wval = weight(x)
        phi = self.phi_output(x)
        g = (np.dot(wval.transpose(), self.theta)).transpose()  # [numFeats x Ns]
        out = np.sum(phi * g, axis=0) / np.sum(phi, axis=0)
        return out

    def feature(self, x, idx):
        """
         Get the output of the idx^th feature for a given input variable(s)

         :param x: a single or vector of dependent variables with size [Ns] for which to calculate the FA features
         :param idx: index of the feature

         :returns: a vector of values
         """
        return np.dot(weight(x)[:, 0], self.theta[:, idx])

    # ----------------------#
    # # Training Algorithm ##
    # ----------------------#

    def train_lwls(self, x_data, y_data):
        
        X = np.array(x_data)
        Y = np.array(y_data)
        w = weight(X)
        phi = self.phi_output(X)
        
        for i in range(self.nb_features):
            
            print(phi[i].shape)
            print(w.shape)
            print(Y.shape)
            
            print(np.dot(phi[i],w.T))
            
            self.theta[0,i] = np.sum(np.dot(np.dot(phi[i],w.T),w))
            self.theta[1,i] = np.sum(np.dot(np.dot(phi[i],w.T),Y))
            

    def plot(self, x_data, y_data):
        xs = np.linspace(0.0, 1.0, 1000)
        z = self.f(xs)

        plt.plot(x_data, y_data, 'o', markersize=3, color='lightgreen')
        plt.plot(xs, z, lw=2, color='red')
        for i in range(self.nb_features):
            ww = (1.0 - 0.0) / self.nb_features / 2.
            xstmp = np.linspace(self.centers[i] - ww, self.centers[i] + ww, 100)

            z2 = []
            for j in xstmp:
                z2.append(self.feature(j, i))
            plt.plot(xstmp, z2, lw=2, color='blue', ls='-')
        plt.show()
