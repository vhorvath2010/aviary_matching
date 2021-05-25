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
    print("Computing differences for", label)
    specs = specs_dict[label]
    avg_diffs = []
    for i in range(len(specs) - 1):
        avg_diff = find_average_diff(specs[i], specs[i + 1])
        avg_diffs.append(avg_diff)
    print("Average difference", sum(avg_diffs) / len(avg_diffs))
