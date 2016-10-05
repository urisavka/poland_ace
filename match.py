import random
import copy

from firm import Firm

def match(firms, entrance_rate):
    new_firms = copy.deepcopy(firms)
    for i in range(abs(int(entrance_rate))):
        employer = new_firms[random.randint(0, len(new_firms) - 1)]
        # employer = numpy.random.choice(self.firms, replace=False)
        # print("Step " + str(self.t) + " Employer " + str(i) + " " + str(employer.workers))
        # TODO: make choice proportional to size of firm instead of uniform
        # employer = numpy.random.choice(self.firms, replace=False, p= workers / sum(workers))
        if entrance_rate > 0:
            employer.workers += 1
        else:
            if employer.workers - 1 > 0:
                employer.workers -= 1
            else:
                i -= 1
    return new_firms