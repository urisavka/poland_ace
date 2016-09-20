from world import World

from sklearn import linear_model
from sklearn.metrics import r2_score

import pandas
import random
from mape import mape

import csv

class Scenario():
    def __init__(self, history, firm_info, regression_type = "total", distribute_subsidies = False, disturb_result = False,
                 disturb_coefficients = False, log_regression = False):
        self.history = pandas.read_csv(history, sep = ";", decimal = ",")
        self.firm_info = firm_info
        self.regression_type = regression_type
        self.disturb_result = disturb_result
        self.disturb_coefficients = disturb_coefficients
        self.log_regression = log_regression
        self.distribute_subsidies = distribute_subsidies
        if self.regression_type == 'average':
            self.model = World(self.history['employees'][0], self.firm_info, self.history[['workers', 'subsidies', 'sales']],
                               distribute_subsidies, disturb_result, disturb_coefficients, log_regression, regression_type)
        else:
            self.model = World(self.history['employees'][0], self.firm_info, self.history[['employees', 'budget', 'revenues']],
                               distribute_subsidies, disturb_result, disturb_coefficients, log_regression, regression_type)

        self.benchmark = self.history['revenues']
        self.workers_history = self.history['employees']
        self.budget_history = self.history['budget']
        with open("output.csv", "w") as self.output_file:
            writer = csv.DictWriter(self.output_file, delimiter = ';',
                                    fieldnames=["step", "regression_type", "distribute_subsidies", "disturb_result",
                                                "disturb_coefficients", "mape", "r2_score"])
            writer.writeheader()
        self.output_file.close()
        self.output_file = open("output.csv", "a")
        self.output_writer = csv.writer(self.output_file, delimiter = ';')


    def run(self, steps):
        for step in range(steps):
            self.model.step(self.budget_history[step], self.workers_history[step])
            print("Step " + str(step + 1) + " finished.")
            self.output_writer.writerow((step, self.regression_type, self.distribute_subsidies, self.disturb_result, self.disturb_coefficients,
                                mape(self.benchmark[:len(self.model.sales)], self.model.sales),
                                r2_score(self.benchmark[:len(self.model.sales)], self.model.sales)))
#            sales_file.write("%.2f" % poland.sales[step] + '\n')
#            workers_file.write(str(poland.workers[step]) + '\n')
#            rscore_file.write("%.4f" % rscore + '\n')
#            mape_file.write("%.4f" % mape_score + '\n')


