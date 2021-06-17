import math

import numpy as np
import csv
import matplotlib.pyplot as plt

# Load probabilities
probabilities = np.load("matches/grouped_audio.npy")
# Load actual songs
songs_order = []
with open('data/grouped_audio_annotations.csv') as csvfile:
    reader = csv.reader(csvfile)
    first_row = True
    for row in reader:
        if first_row:
            first_row = False
            continue
        label = float(row[0])
        label = math.floor(label)
        songs_order.append(label)
# Search probabilities for highest value of song X at the times song X is playing
predictions_per_song = len(probabilities[0]) / len(songs_order)
highest_probs = []
for i in range(len(songs_order)):
    song = songs_order[i]
    highest_prob = 0
    for prob_index in range(math.floor(i * predictions_per_song), math.floor((i + 1) * predictions_per_song)):
        prob = probabilities[song][prob_index]
        highest_prob = max(highest_prob, prob)
    highest_probs.append(highest_prob)
print(np.average(highest_probs))
