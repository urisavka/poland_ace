from sklearn import linear_model
import random
import pandas
import numpy

from firm import Firm

def create_firms(firm_info, history, clf):
    firms = []
    for info in firm_info:
        for number in range(info['number']):
            firms.append(Firm(random.normalvariate(info['workers'], 10), clf, history))
    return firms


class World:
    def __init__(self, entrance_rate, firm_info, history, workers):
        self.clf = linear_model.BayesianRidge(compute_score = True, normalize = True)
        self.clf.fit(history[['workers', 'subsidies']], history['sales'])
        self.entrance_rate = entrance_rate
        self.workers = workers
        self.firms = create_firms(firm_info, history, self.clf, workers)

    def step(self, subsidies):
        self.workers += self.entrance_rate
        self.match()
        for firm in self.firms:
            firm.step(subsidies)

    def match(self):
        for i in range(self.entrance_rate):
            employer = numpy.random.choice(self.firms, replace=False)
            #TODO: make choice proportional to size of firm instead of uniform
            #employer = numpy.random.choice(self.firms, replace=False, p= workers / sum(workers))
            employer.workers += 1



