import numpy as np

class Gaussians:
    def __init__(self, nb_features):
        self.nb_features = nb_features
        self.centers = np.linspace(0.0, 1.0, self.nb_features)
        width_constant = (1.0 - 0.0) / self.nb_features / 10
        self.widths = np.ones(self.nb_features, ) * width_constant

    def phi_output(self, x):
        """
        Get the output of the Gaussian features for a given input variable(s)

        :param x: A single or vector of dependent variables with size [Ns] for which to calculate the features

        :returns: A vector of feature outputs with size [NumFeats x Ns]
        """
        if np.size(x) == 1:
            return np.exp(-np.divide(np.square(x - self.centers), self.widths))
        elif np.size(x) > 1:
            num_evals = np.shape(x)[0]
            # Repeat vectors to vectorize output calculation
            input_mat = np.array([x, ] * self.nb_features)
            centers_mat = np.array([self.centers, ] * num_evals).transpose()
            widths_mat = np.array([self.widths, ] * num_evals).transpose()
            return np.exp(-np.divide(np.square(input_mat - centers_mat), widths_mat))
