from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
import random
import pandas
import numpy
import copy
import math

from firm import Firm

class World:
    def other__init__(self, employees, firm_info, history, distribute_subsidies, disturb_result, disturb_coefficients, regression,
                 regression_type):
        self.distribute_subsidies = distribute_subsidies
        self.disturb_result = disturb_result
        self.disturb_coefficients = disturb_coefficients
        self.regression = regression

        self.history = history
        if regression_type == 'total':
            self.history.rename(index=str, columns={"employees": "workers", "budget": "subsidies", "revenues": "sales"},
                                               inplace = True)
        if regression == 'bayes':
            self.clf = linear_model.BayesianRidge(compute_score = True, fit_intercept=False)
            self.clf.fit(self.history[['workers', 'subsidies']], self.history['sales'])
        elif regression == 'linear':
            self.clf = linear_model.LinearRegression(fit_intercept=False)
            self.clf.fit(self.history[['workers', 'subsidies']], self.history['sales'])
        elif regression == 'loglinear':
            self.history['product'] = self.history.workers.mul(self.history.subsidies)
            self.history['log_product'] = self.history['product'].apply(math.log)
            self.history['log_sales'] = self.history['sales'].apply(math.log)
            self.clf = linear_model.LinearRegression(fit_intercept=True)
            self.clf.fit(self.history[['log_product']], self.history[['log_sales']])
        self.create_firms(firm_info, self.history, self.clf, employees, disturb_result, disturb_coefficients, regression)
        self.employees = employees
        self.sales = []
        self.workers = []
        self.t = 0

    def __init__(self, employees, firm_info, history, distribute_subsidies, disturb_result, disturb_coefficients,
                     regression, regression_type, match_info, distribute_subsidies_info):

        self.distribute_subsidies = distribute_subsidies
        self.disturb_result = disturb_result
        self.disturb_coefficients = disturb_coefficients
        self.regression = regression

        self.history = history
        if regression_type == 'total':
            self.history.rename(index=str, columns={"employees": "workers", "budget": "subsidies", "revenues": "sales"},
                                inplace=True)
        if regression == 'bayes':
            self.clf = linear_model.BayesianRidge(compute_score=True, fit_intercept=False)
            self.clf.fit(self.history[['workers', 'subsidies']], self.history['sales'])
        elif regression == 'linear':
            self.clf = linear_model.LinearRegression(fit_intercept=False)
            self.clf.fit(self.history[['workers', 'subsidies']], self.history['sales'])
        elif regression == 'loglinear':
            self.history['product'] = self.history.workers.mul(self.history.subsidies)
            self.history['log_product'] = self.history['product'].apply(math.log)
            self.history['log_sales'] = self.history['sales'].apply(math.log)
            self.clf = linear_model.LinearRegression(fit_intercept=True)
            self.clf.fit(self.history[['log_product']], self.history[['log_sales']])
        self.firms = firm_info
        self.set_parameters()
        self.employees = employees
        self.sales = []
        self.workers = []
        self.t = 0
        self.match_info = match_info
        self.distribute_subsidies_info = distribute_subsidies_info

    def set_parameters(self):
        for firm in self.firms:
            firm_clf = copy.deepcopy(self.clf)
            if self.disturb_coefficients:
                firm_clf.coef_[0] += random.normalvariate(0, 0.1 * self.clf.coef_[0])
                if len(firm_clf.coef_) > 1:
                    firm_clf.coef_[1] += random.normalvariate(0, 0.1 * self.clf.coef_[1])
            firm.clf = firm_clf
            firm.disturb_result = self.disturb_result
            firm.regression = self.regression

    def update_firms(self):
        for i, firm in enumerate(self.firms):
            workers = self.match_info[self.t][i].workers
            if workers > 0:
                firm.workers = workers
            else:
                self.firms.remove(firm)



    def create_firms(self, firm_info, history, clf, employees, disturb_result, disturb_coefficients, regression):
        self.firms = []
        i = 0
        for index, info in firm_info.iterrows():
            for number in range(int(info['number'])):
                firm_clf = copy.deepcopy(clf)
                if disturb_coefficients:
                    firm_clf.coef_[0]+= random.normalvariate(0, 0.1 * clf.coef_[0])
                    if len(firm_clf.coef_) > 1:
                        firm_clf.coef_[1] += random.normalvariate(0, 0.1 * clf.coef_[1])
                while True:
                    workers = int(random.normalvariate(float(info['workers']), float(info['sd'])))
                    if workers > 0:
                        break
                self.firms.append(
                    Firm(i, workers, firm_clf, history, disturb_result,
                         regression))
                i += 1
        workers = sum([firm.workers for firm in self.firms])
        for firm in self.firms:
            firm.workers = int(firm.workers / workers * employees)

    def step(self, subsidies, employees):
        if not hasattr(self, 'match_info'):
            self.match(employees)
        else:
            self.update_firms()
        print("Match employees finished")
        sold = 0
        workers = 0
        if self.distribute_subsidies:
            #distributed_subsidies = self.distribute_funding(subsidies)
            distributed_subsidies = self.distribute_subsidies_info[self.t]
        else:
            distributed_subsidies = [subsidies/len(self.firms)] * len(self.firms)
        for i, firm in enumerate(self.firms):
            firm.step(distributed_subsidies[i])
            sold += firm.sales
            workers += firm.workers
        self.sales.append(sold)
        self.workers.append(workers)
        self.t += 1

    def distribute_funding(self, subsidies):
        distributed_subsidies = []
        subsidies_mean = self.history['subsidies'].mean()
        subsidies_sd = self.history['subsidies'].std()
        for firm in self.firms:
            new_subsidy = random.normalvariate(subsidies_mean, subsidies_sd)
            new_subsidy = new_subsidy if new_subsidy > 0 else 0
            distributed_subsidies.append(new_subsidy)
        total = sum(distributed_subsidies)
        total = total if total != 0 else 1
        for i in range(len(distributed_subsidies)):
            distributed_subsidies[i] = distributed_subsidies[i] * subsidies / total
        return distributed_subsidies

    def match(self, employees):
        entrance_rate = employees - self.employees
        print("Entrance rate: " + str(entrance_rate))
        self.employees += entrance_rate
        for i in range(abs(int(entrance_rate))):
            employer = self.firms[random.randint(0, len(self.firms) - 1)]
            #employer = numpy.random.choice(self.firms, replace=False)
            print("Step " + str(self.t) + " Employer " + str(i) + " " + str(employer.workers))
            #TODO: make choice proportional to size of firm instead of uniform
            #employer = numpy.random.choice(self.firms, replace=False, p= workers / sum(workers))
            if entrance_rate > 0:
                employer.workers += 1
            else:
                if employer.workers - 1 > 0:
                    employer.workers -= 1
                else:
                    i -= 1
                    self.firms.remove(employer)






