#!/usr/local/bin/python

import numpy as np
import time
from rbfn import RBFN
from lwr import LWR
from line import Line
from sample_generator import generate_non_linear_samples, generate_linear_samples


class Main:
    def __init__(self):
        self.x_data = []
        self.y_data = []

    def reset_batch(self):
        self.x_data = []
        self.y_data = []

    def make_nonlinear_batch_data(self):
        """ 
        Generate a batch of non linear data and store it
        """
        self.reset_batch()
        batch_size = 1000
        for i in range(batch_size):
            # Draw a random sample on the interval [0,1]
            x = np.random.random()
            y = generate_non_linear_samples(x)
            self.x_data.append(x)
            self.y_data.append(y)

    def make_linear_batch_data(self):
        """ 
        Generate a batch of linear data and store it
        """
        self.reset_batch()
        batch_size = 1000
        for i in range(batch_size):
            # Draw a random sample on the interval [0,1]
            x = np.random.random()
            y = generate_linear_samples(x)
            self.x_data.append(x)
            self.y_data.append(y)

    def approx_linear_batch(self):
        model = Line(batch_size=50)

        self.make_linear_batch_data()


        start = time.process_time()
        model.train_ls(self.x_data, self.y_data)
        print("time:", time.process_time() - start)
        model.plot(self.x_data, self.y_data)
        
        model.train_from_stats(self.x_data, self.y_data)
        model.plot(self.x_data, self.y_data)
        model.train_regularized(self.x_data, self.y_data, coef=0.9)
        model.plot(self.x_data, self.y_data)

    def approx_rbfn_batch(self):
        model = RBFN(nb_features=30)
        self.make_nonlinear_batch_data()

        start = time.process_time()
        model.train_ls(self.x_data, self.y_data)
        print("time:", time.process_time() - start)
        model.plot(self.x_data, self.y_data)

    def approx_rbfn_iterative(self):
        max_iter = 1000
        model = RBFN(nb_features=12)
        start = time.process_time()
        # Generate a batch of data and store it
        self.reset_batch()
        for i in range(max_iter):
            # Draw a random sample on the interval [0,1]
            x = np.random.random()
            y = generate_non_linear_samples(x)
            self.x_data.append(x)
            self.y_data.append(y)

            # Comment the ones you don't want to use
            # model.train_rls(x, y)
            # model.train_rls2(x, y)
            model.train_gd(x, y, alpha=0.5)
        print("time:", time.process_time() - start)
        model.plot(self.x_data, self.y_data)

    def approx_lwr_batch(self):
        model = LWR(nb_features=10)
        self.make_nonlinear_batch_data()

        start = time.process_time()
        model.train_lwls(self.x_data, self.y_data)
        print("time:", time.process_time() - start)
        model.plot(self.x_data, self.y_data)


m = Main()
m.approx_linear_batch()
#m.approx_rbfn_batch()
#m.approx_rbfn_iterative()
#m.approx_lwr_batch()
