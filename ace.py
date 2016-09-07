import pandas

#datafile = "C:\Diana\Poland\Poland\poland_aggregate.csv"
datafile = "C:/Users/d.omelianchyk/Downloads/poland.csv"
#datafile = "D:\Poland\poland.csv"
history = pandas.read_csv(datafile, sep = ";", decimal = ",")

#datafile = "D:\Poland\poland_info.csv"
datafile = "C:/Users/d.omelianchyk/Downloads/poland_info.csv"
firm_info = pandas.read_csv(datafile, sep = ";", decimal = ",")

print(history)
print(firm_info)


from sklearn import linear_model

#clf = linear_model.BayesianRidge(compute_score= True)
clf = linear_model.LinearRegression()
clf.fit(history[['workers', 'subsidies']], history['sales'])

print(clf.score(history[['workers', 'subsidies']], history['sales']))

from world import World

poland = World(216, firm_info, history, 2177153)

steps = 12

sales_file = open("sales.txt", "w")
workers_file = open("workers.txt", "w")

for step in range(steps):
    poland.step(50)
    sales_file.write("%.2f" % poland.sales[step]+ '\n')
    workers_file.write(str(poland.workers[step]) + '\n')

sales_file.close()
workers_file.close()

import matplotlib.pyplot as plt

plt.figure(figsize=(6, 5))
plt.title("Sales")
plt.plot(poland.sales, 'b-', label="Sales")
plt.ylim(ymin = 0)

plt.figure(figsize=(6, 5))
plt.title("Workers")
plt.plot(poland.workers, 'b-', label="Workers")
plt.show()
