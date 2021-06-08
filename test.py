import numpy as np


def find_sim(template, section):
    # Scale spectrogram so max values are 1
    max_temp = np.max(template)
    template = np.divide(template, max_temp)
    max_sec = np.max(section)
    section = np.divide(section, max_sec)
    # Find differences
    diff = abs(section - template)
    # Subtract from array of 1's to get similarities
    sim = abs(np.ones(template.shape) - diff)
    # Return average similarity
    return sum(sum(sim)) / (len(sim) * len(sim[0]))


a = 10 * np.asarray([[1, 2, 0], [0, 0, 1], [1, 0, 0]])
b = 10 * np.asarray([[1, 2, 0], [0, 0, 1], [1, 0, 0]])
print(find_sim(a, b))
