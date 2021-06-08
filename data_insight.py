import os
import numpy as np


def find_average_diff(spec_a, spec_b):
    diff = abs(spec_a - spec_b)
    # Try returning raw diff
    # return sum(sum(diff)) / (len(diff) * len(diff[0]))
    # Find total percentages and average percentage difference
    avg = (spec_a + spec_b) / 2
    perc_diff = 100 * abs(diff / avg)
    total_diff = sum(sum(perc_diff))
    average_diff = total_diff / (len(diff) * len(diff[0]))
    return average_diff


def find_sim(template, section):
    # Scale spectrogram so max values are 1
    max_temp = np.max(template)
    template = np.divide(template, max_temp)
    max_sec = np.max(section)
    section = np.divide(section, max_sec)
    # Find differences
    diff = abs(section - template)
    # Subtract from array of 1's to get similarities
    curr_sim = np.ones(template.shape) - diff
    # Return average similarity
    return sum(sum(curr_sim)) / (len(curr_sim) * len(curr_sim[0]))


# Load spectrogram dictionary
labels = [i for i in range(23)]
specs_dict = {}
for label in labels:
    label_dir = 'specs/' + str(label)
    specs_dict[label] = []
    print('Loading specs for', label)
    for filename in os.listdir(label_dir):
        path = label_dir + "/" + filename
        spec = np.load(path)
        specs_dict[label].append(spec)
    print('Loaded', len(specs_dict[label]), 'specs')

# Compare similarities between samples of same song (simple previous, next, approach)
for label in specs_dict.keys():
    print("Computing similarities for", label)
    specs = specs_dict[label]
    sims = []
    for i in range(len(specs) - 1):
        sim = find_sim(specs[i], specs[i + 1])
        sims.append(sim)
    print("Average similarity", sum(sims) / len(sims))

print("Sim for random two", find_sim(specs_dict[16][4], specs_dict[5][7]))
