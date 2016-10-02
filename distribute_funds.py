import random

def distribute_funding(history, subsidies, firm_number):
    distributed_subsidies = []
    subsidies_mean = history['subsidies'].mean()
    subsidies_sd = history['subsidies'].std()
    for i in range(firm_number):
        new_subsidy = random.normalvariate(subsidies_mean, subsidies_sd)
        new_subsidy = new_subsidy if new_subsidy > 0 else 0
        distributed_subsidies.append(new_subsidy)
    total = sum(distributed_subsidies)
    total = total if total != 0 else 1
    for i in range(firm_number):
        distributed_subsidies[i] = distributed_subsidies[i] * subsidies / total
    return distributed_subsidies
