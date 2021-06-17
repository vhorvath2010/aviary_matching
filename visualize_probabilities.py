import matplotlib.pyplot as plt
import numpy as np

probabilities = np.load("matches/test_audio.npy")
songs_labels = [i for i in range(23)]
times = [i for i in range(len(probabilities[0]))]
plt.pcolormesh(np.array(times) / 93.75, songs_labels, probabilities, shading='nearest')
plt.ylabel('Song Type')
plt.xlabel('Time (seconds)')
plt.title('Test Audio Probabilities (Method 3 Mask)')
plt.show()
