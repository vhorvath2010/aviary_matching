import numpy as np
import csv

probabilities = np.load("matches/grouped_audio.npy")
with open('data/grouped_audio_annotations.csv') as csvfile:
    reader = csv.reader(csvfile)
    first_row = True
    song = 0
    for row in reader:
        if first_row:
            first_row = False
            continue
        label = float(row[0])
