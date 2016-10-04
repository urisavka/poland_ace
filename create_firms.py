import random
import copy
import math

from firm import Firm

def create_firms(firm_info, employees):
    firms = []
    i = 0
    for index, info in firm_info.iterrows():
        for number in range(int(info['number'])):
            while True:
                workers = int(random.normalvariate(float(info['workers']), float(info['sd'])))
                if workers > 0:
                    break
            firms.append(
                Firm(i, workers))
            i += 1
    workers = sum([firm.workers for firm in firms])
    for firm in firms:
        firm.workers = int(round(firm.workers / workers * employees, 0))
    workers = sum([firm.workers for firm in firms])
    while workers != employees:
        employer = firms[random.randint(0, len(firms) - 1)]
        if workers > employees and employer.workers - 1 > 0:
            employer.workers -= 1
        else:
            employer.workers += 1
        workers = sum([firm.workers for firm in firms])
    return firms