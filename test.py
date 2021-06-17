import numpy as np


def find_mask_sim(template, section):
    # Create masks
    t_mask = template > 0
    s_mask = section > 0
    # Return ratio of overlapping segments
    return sum(sum(np.logical_and(t_mask, s_mask))) / sum(sum(t_mask))


a = 10 * np.asarray([[1, 0, 0], [0, 0, 1], [1, 0, 0]])
b = 10 * np.asarray([[0, 2, 0], [0, 1, 0], [0, 1, 0]])
print(find_mask_sim(a, b))
