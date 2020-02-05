import numpy as np
import matplotlib.pyplot as plt
from gaussians import Gaussians


class RBFN(Gaussians):
    def __init__(self, nb_features):
        super().__init__(nb_features)
        self.theta = np.random.random(self.nb_features)
        self.a = np.zeros(shape=(self.nb_features, self.nb_features))
        self.a_inv = np.matrix(np.identity(self.nb_features))
        self.b = np.zeros(self.nb_features)

    def f(self, x, *user_theta):
        """
        Get the FA output for a given input variable(s)
    
        :param x: A single or vector of dependent variables with size [Ns] for which to calculate the FA features
        :param user_theta: (Variable argument) A vector of theta variables to apply to the FA. 
        :If left blank the method will default to using the trained thetas in self.theta. 
        :This is only used for visualization purposes.
        
        :returns: A vector of function approximator outputs with size [Ns]
        """
        phi = self.phi_output(x)
        if not user_theta:
            temp = self.theta
        else:
            temp = np.array(user_theta)
        out = np.dot(phi, temp.transpose())
        return out

    def feature(self, x, idx):
        """
         Get the output of the idx^th feature for a given input variable(s)
         Used mainly for plotting

         :param x: A single or vector of dependent variables with size [Ns] for which to calculate the FA features
         :param idx: index of the feature

         :returns: a value
         """
        phi = self.phi_output(x)
        return phi[idx] * self.theta[idx]

    # ----------------------#
    # # Training Algorithms ##
    # ----------------------#

    def train_ls(self, x_data, y_data):
        #Fill this part
        
        phi = self.phi_output(x_data)
        
        B = np.dot(phi,y_data)
        A = np.linalg.pinv(np.dot(phi,phi.T))
        self.theta = np.dot(A,B)

    def train_rls(self, x, y):
        #Fill this part
        for i in range(self.nb_features):
            self.theta[i] = 0#fill this

    def train_rls2(self, x, y):
        #Fill this part
        for i in range(self.nb_features):
            self.theta[i] = 0#fill this

    def train_gd(self, x, y, alpha):
        
        phi = self.phi_output(x)
        eps = y - self.f(x)
        self.theta = self.theta+alpha*eps*phi

    # -----------------#
    # # Plot function ##
    # -----------------#

    def plot(self, x_data, y_data):
        xs = np.linspace(0.0, 1.0, 1000)
        z = []
        for i in xs:
            z.append(self.f(i))

        z2 = []
        for i in range(self.nb_features):
            temp = []
            for j in xs:
                temp.append(self.feature(j, i))
            z2.append(temp)

        plt.plot(x_data, y_data, 'o', markersize=3, color='lightgreen')
        plt.plot(xs, z, lw=3, color='red')
        for i in range(self.nb_features):
            plt.plot(xs, z2[i])
        plt.show()
