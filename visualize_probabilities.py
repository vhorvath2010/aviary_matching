import matplotlib.pyplot as plt
import numpy as np

probabilities = np.load("matches/grouped_audio.npy")
songs_labels = [i for i in range(23)]
times = [i for i in range(len(probabilities[0]))]
plt.pcolormesh(times, songs_labels, probabilities, shading='auto')
plt.ylabel('Song Type')
plt.xlabel('Guess Number')
plt.title('Grouped Audio Probabilities (Method 1)')
plt.show()
