import math
import os
from scipy import signal
from scipy.io import wavfile
import numpy as np
import csv
import matplotlib.pyplot as plt

# Load sound data and convert to mono
sr, stereo_samples = wavfile.read('data/grouped_audio.wav')
mono_samples = np.array(stereo_samples)
mono_samples = mono_samples.transpose()
mono_samples = ((mono_samples[0] + mono_samples[1])/2)


# Create spectrogram for each label

with open('data/grouped_audio_annotations.csv') as csvfile:
    reader = csv.reader(csvfile)
    first_row = True
    spec = 0
    for row in reader:
        if first_row:
            first_row = False
            continue
        spec += 1
        label = float(row[0])
        label = str(math.floor(label))
        start = float(row[1])
        stop = float(row[2])
        # Change start and stop to samples
        start = math.floor(start * sr)
        stop = math.ceil(stop * sr)
        frequencies, times, spectrogram = signal.spectrogram(mono_samples[start:stop], sr, nperseg=512, noverlap=384)
        # Save spectrogram to np array
        np_spectrogram = np.array(spectrogram)
        np_frequencies = np.array(frequencies)
        np_times = np.array(times)
        # Create directory if needed and save spec data
        label_path = os.path.join('specs', label)
        if not os.path.exists(label_path):
            os.mkdir(label_path)
        # Turn to True to see graphed spectrograms
        if False:
            plt.pcolormesh(times, frequencies, spectrogram, shading='gouraud')
            plt.ylabel('Frequency [Hz]')
            plt.xlabel('Time [sec]')
            plt.show()
        np.save(os.path.join(label_path, str(spec)), np_spectrogram)