from world import World

import mape

from sklearn import linear_model
from sklearn.metrics import r2_score

import pandas
import random

import matplotlib.pyplot as plt

class Scenario():
    def __init__(self, history, firm_info, regression_type = "total", disturb_result = False,
                 disturb_coefficients = False, log_regression = False):
        self.history = pandas.read_csv(history, sep = ";", decimal = ",")
        self.firm_info = firm_info
        self.regression_type = regression_type
        self.disturb_result = disturb_result
        self.disturb_coefficients = disturb_coefficients
        self.log_regression = log_regression
        if regression_type == 'average':
            self.model = World(self.history['employees'][0], self.firm_info, self.history[['workers', 'subsidies', 'sales']])
        else:
            self.model = World(self.history['employees'][0], self.firm_info,
                               self.history[['employees', 'budget', 'revenues']])

    def run(self, steps):
        for step in range(steps):
            self.model.step(history['budget'][step], history['employees'][step])
            print("Step " + str(step + 1) + " finished.")
            sales_file = open("sales.txt", "a")
            workers_file = open("workers.txt", "a")
            rscore_file = open("rscore.txt", "a")
            mape_file = open("mape.txt", "a")
            rscore = r2_score(history['revenues'][:len(poland.sales)], poland.sales)
            mape_score = mape(history['revenues'][:len(poland.sales)], poland.sales)
            print(rscore)
            print(mape_score)
            sales_file.write("%.2f" % poland.sales[step] + '\n')
            workers_file.write(str(poland.workers[step]) + '\n')
            rscore_file.write("%.4f" % rscore + '\n')
            mape_file.write("%.4f" % mape_score + '\n')


