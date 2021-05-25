import os
import wave

import numpy as np
from scipy import signal
from scipy.io import wavfile


def find_average_diff(spec_a, spec_b):
    diff = abs(spec_a - spec_b)
    avg = (spec_a + spec_b) / 2
    perc_diff = 100 * abs(diff / avg)
    total_diff = sum(sum(perc_diff))
    average_diff = total_diff / (len(diff) * len(diff[0]))
    return average_diff


# Get user parameters
file_dir = input("Enter the relative path of the file for searching: ")
song_type = input("Enter the song type to search for: ")

# Load song templates
spec_dir = 'specs/' + song_type
specs = []
print("Loading spectrograms for", song_type)
for filename in os.listdir(spec_dir):
    path = spec_dir + "/" + filename
    specs.append(np.load(path))
print("Loaded", len(specs), "spectrograms")

# Load audio data for comparison
print("Loading audio data for searching")
sr, stereo_samples = wavfile.read(file_dir)
mono_samples = np.array(stereo_samples)
mono_samples = mono_samples.transpose()
mono_samples = ((mono_samples[0] + mono_samples[1])/2)
audio_len = len(mono_samples) / sr
# Create spectrogram of the audio data, and flip so x axis is time
frequencies, times, spectrogram = signal.spectrogram(mono_samples, sr, nperseg=512, noverlap=384)
np_spectrogram = np.array(spectrogram)
np_spectrogram = np_spectrogram.transpose()
print("Audio data loaded")

# Search for matches
print("Searching for segments of song", song_type, "in audio")
template_spec = specs[0]
template_spec = template_spec.transpose()
matches = []
for starting_point in range(0, len(np_spectrogram) - len(template_spec), 16):
    comparison_spec = np_spectrogram[starting_point:starting_point + len(template_spec)]
    avg_diff = find_average_diff(template_spec, comparison_spec)
    if avg_diff <= 125:
        starting_time = starting_point / len(np_spectrogram) * audio_len
        print("Match found at", starting_time, "seconds")
        matches.append(starting_time * sr)
