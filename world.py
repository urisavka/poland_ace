from sklearn import linear_model
import random
import pandas
import numpy

from firm import Firm

def create_firms(firm_info, history, clf):
    firms = []
    for index, info in firm_info.iterrows():
        for number in range(int(info['number'])):
            firms.append(Firm(random.normalvariate(float(info['workers']), float(info['sd'])), clf, history))
    return firms


class World:
    def __init__(self, entrance_rate, firm_info, history, workers):
        self.clf = linear_model.BayesianRidge(compute_score = True, normalize = True)
        self.clf.fit(history[['workers', 'subsidies']], history['sales'])
        self.entrance_rate = entrance_rate
        self.firms = create_firms(firm_info, history, self.clf)
        self.sales = []
        self.workers = []

    def step(self, subsidies):
        self.match()
        sold = 0
        workers = 0
        for firm in self.firms:
            firm.step(subsidies)
            sold += firm.sales
            workers += firm.workers
        self.sales.append(sold)
        self.workers.append(workers)




    def match(self):
        for i in range(self.entrance_rate):
            employer = numpy.random.choice(self.firms, replace=False)
            #TODO: make choice proportional to size of firm instead of uniform
            #employer = numpy.random.choice(self.firms, replace=False, p= workers / sum(workers))
            employer.workers += 1





