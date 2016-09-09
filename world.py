from sklearn import linear_model
import random
import pandas
import numpy

from firm import Firm

def create_firms(firm_info, history, clf, employees):
    firms = []
    for index, info in firm_info.iterrows():
        for number in range(int(info['number'])):
            firms.append(Firm(random.normalvariate(float(info['workers']), float(info['sd'])), clf, history))
    workers = sum([firm.workers for firm in firms])
    for firm in firms:
        firm.workers = int(firm.workers/workers * employees)
    return firms


class World:
    def __init__(self, employees, firm_info, history):
        self.clf = linear_model.BayesianRidge(compute_score = True)
        self.clf.fit(history[['workers', 'subsidies']], history['sales'])
        self.firms = create_firms(firm_info, history, self.clf, employees)
        self.employees = employees
        self.sales = []
        self.workers = []

    def step(self, subsidies, employees):
        self.match(employees)
        print("Match employees finished")
        sold = 0
        workers = 0
        for firm in self.firms:
            firm.step(subsidies)
            sold += firm.sales
            workers += firm.workers
        self.sales.append(sold)
        self.workers.append(workers)




    def match(self, employees):
        entrance_rate = employees - self.employees
        print("Entrance rate: " + str(entrance_rate))
        self.employees += entrance_rate
        for i in range(abs(int(entrance_rate))):
            employer = numpy.random.choice(self.firms, replace=False)
            print("Employer " + str(i) + " " + str(employer.workers))
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






