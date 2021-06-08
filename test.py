import numpy as np


def find_sim(template, section):
    perc_diff = abs(section - template)
    ones = np.ones(template.shape)
    sim = ones - perc_diff
    print(sim)
    total_sim = sum(sum(sim))
    return total_sim/len(sim)


a = np.asarray([[1, 0, 0], [0, 0, 1], [1, 0, 0]])
b = np.asarray([[.9, 0.1, 0], [0.1, 0.15, 1], [.95, .1, 0]])
print(find_sim(a, b))
