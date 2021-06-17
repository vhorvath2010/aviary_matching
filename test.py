import numpy as np
from scipy import ndimage


def find_mask_sim(template, section):
    # Create masks
    t_mask = np.greater(template, 0)
    s_mask = np.greater(section, 0)
    # Dilate template mask
    t_mask = ndimage.binary_dilation(t_mask)
    # Return ratio of overlapping segments
    return np.sum(np.logical_and(t_mask, s_mask)) / t_mask.sum()


a = np.asarray([[0, 0, 0], [0, 0, 1], [0, 0, 0]])
b = np.asarray([[1, 0, 0], [0, 0, 1], [1, 0, 0]])
print(find_mask_sim(a, b))
