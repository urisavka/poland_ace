import pandas
import random

#datafile = "C:\Diana\Poland\Poland\poland_aggregate.csv"
#datafile = "C:/Users/d.omelianchyk/Downloads/poland.csv"
datafile = "poland.csv"
history = pandas.read_csv(datafile, sep = ";", decimal = ",")

datafile = "poland_info_copy.csv"
#datafile = "D:\Poland\poland_info_copy.csv"
#datafile = "C:/Users/d.omelianchyk/Downloads/poland_info.csv"
firm_info = pandas.read_csv(datafile, sep = ";", decimal = ",")

print(history)
print(firm_info)

random.seed(1)

import numpy

def mape(y_pred, y_true):
    res = 0
    for i in range(len(y_true)):
        res += abs((y_pred[i] - y_true[i])/y_true[i])
    return res/len(y_true) * 100


from sklearn import linear_model

clf = linear_model.BayesianRidge(compute_score= True, fit_intercept = False)
#clf = linear_model.LinearRegression()

clf.fit(history[['workers', 'subsidies']], history['sales'])
clf.fit(history[['employees', 'budget']], history['revenues'])

print(clf.score(history[['workers', 'subsidies']], history['sales']))
print(clf.score(history[['employees', 'budget']], history['revenues']))

from world import World
from sklearn.metrics import r2_score

poland = World(history['employees'][0], firm_info, history[['workers', 'subsidies', 'sales']])

steps = 34

sales_file = open("sales.txt", "w")
workers_file = open("workers.txt", "w")
rscore_file = open("rscore.txt", "w")
mape_file = open("mape.txt", "w")
sales_file.close()
workers_file.close()
rscore_file.close()
mape_file.close()

for step in range(steps):
    poland.step(history['budget'][step], history['employees'][step])
    print("Step " + str(step + 1) + " finished." )
    sales_file = open("sales.txt", "a")
    workers_file = open("workers.txt", "a")
    rscore_file = open("rscore.txt", "a")
    mape_file = open("mape.txt", "a")
    rscore = r2_score(history['revenues'][:len(poland.sales)], poland.sales)
    mape_score = mape(history['revenues'][:len(poland.sales)], poland.sales)
    print(rscore)
    print(mape_score)
    sales_file.write("%.2f" % poland.sales[step]+ '\n')
    workers_file.write(str(poland.workers[step]) + '\n')
    rscore_file.write("%.4f" % rscore + '\n')
    mape_file.write("%.4f" % mape_score + '\n')
    sales_file.close()
    workers_file.close()
    rscore_file.close()
    mape_file.close()






import matplotlib.pyplot as plt

plt.figure(figsize=(6, 5))
plt.title("Sales")
plt.plot(poland.sales, 'b-', label="Sales")
#plt.ylim(ymin = 0)

plt.figure(figsize=(6, 5))
plt.title("Workers")
plt.plot(poland.workers, 'b-', label="Workers")
plt.show()
