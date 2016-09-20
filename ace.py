from scenario import Scenario

import pandas
import random

import matplotlib.pyplot as plt

#datafile = "C:\Diana\Poland\Poland\poland_aggregate.csv"
#datafile = "C:/Users/d.omelianchyk/Downloads/poland.csv"
datafile = "poland.csv"
#history = pandas.read_csv(datafile, sep = ";", decimal = ",")

#datafile = "poland_info_copy.csv"
#datafile = "D:\Poland\poland_info_copy.csv"
#datafile = "C:/Users/d.omelianchyk/Downloads/poland_info.csv"
firm_info = pandas.read_csv("poland_info_copy.csv", sep = ";", decimal = ",")

print(firm_info)

random.seed(1)

steps = 34

scenario = Scenario("poland.csv", firm_info)

scenario.run(steps)




#plt.figure(figsize=(6, 5))
#plt.title("Sales")
#plt.plot(poland.sales, 'b-', label="Sales")
#plt.ylim(ymin = 0)

#plt.figure(figsize=(6, 5))
#plt.title("Workers")
#plt.plot(poland.workers, 'b-', label="Workers")
#plt.show()
