from sklearn import linear_model
import random
import pandas
import time

class Firm:
    def __init__(self, i, workers, clf, history, disturb_result):
        self.id = i
        self.workers = workers
        self.clf = clf
        self.history = history
        self.disturb_result = disturb_result
#        random.seed(1)

    def step(self, subsidies):
        print("Firm step " + str(time.time()))
        self.sales = self.clf.predict([[self.workers, subsidies]])
        if self.disturb_result:
            self.sales += random.normalvariate(0, 0.05 * self.sales)
        #self.sales = self.clf.predict([[self.workers, subsidies]])
        self.sales = self.sales if self.sales > 0 else 0
        #self.history.loc[-1] = [self.workers, subsidies, self.sales]
        #self.history.index = self.history.index + 1
        #self.clf.fit(self.history[['workers', 'subsidies']], self.history['sales'])


