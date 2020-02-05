#!/usr/local/bin/python

import math
import numpy as np

def generate_non_linear_samples(x):
    """
    Generate a noisy nonlinear data sample from a given data point in the range [0,1]

    :param x: A scalar dependent variable for which to calculate the output y_noisy
        
    :returns: The output with Gaussian noise added
            
    """
    y = 1 - x - math.sin(-2 * math.pi * x ** 3) * math.cos(-2 * math.pi * x ** 3) * math.exp(-x ** 4)
    sigma = 0.1
    noise = sigma * np.random.random()
    y_noisy = y + noise
    return y_noisy

def generate_linear_samples(x):
    """
    Generate a noisy linear data sample from a given data point in the range [0,1]

    :param x: A scalar dependent variable for which to calculate the output y_noisy

    :returns: The output with Gaussian noise added

    """
    y = 3 * x - 2
    sigma = 0.5
    noise = sigma * np.random.random()
    y_noisy = y + noise
    return y_noisy
