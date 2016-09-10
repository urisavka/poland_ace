from sklearn import linear_model
import random
import pandas
import time

class Firm:
    def __init__(self, workers, clf, history):
        self.workers = workers
        self.clf = clf
        self.history = history

    def step(self, subsidies):
        print("Firm step " + str(time.time()))
        self.sales = self.clf.predict([[self.workers, subsidies]]) + random.normalvariate(0, self.history['sales'].std())
        self.sales = self.sales if self.sales > 0 else 0
        self.history.update([[self.workers, subsidies, self.sales]])
        self.clf.fit(self.history[['workers', 'subsidies']], self.history['sales'])


