import csv
import math

from matplotlib import pyplot as plt

sr = 48000
songs_to_plot = 2749
probabilities = [[0 for i in range(songs_to_plot)] for i in range(23)]
with open('data/grouped_audio_annotations.csv') as csvfile:
    reader = csv.reader(csvfile)
    first_row = True
    spec = 0
    song = 0
    for row in reader:
        if first_row:
            first_row = False
            continue
        spec += 1
        label = float(row[0])
        label = int(math.floor(label))
        probabilities[label][song] = 100
        song += 1
        if song >= songs_to_plot:
            break

plt.pcolormesh([i for i in range(songs_to_plot)], [i for i in range(23)], probabilities, shading='nearest')
plt.ylabel('Song Type')
plt.xlabel('Song')
plt.show()
