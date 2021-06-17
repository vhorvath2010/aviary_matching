import math
import os
import numpy as np
from scipy import signal
from scipy.io import wavfile


def find_mask_sim(template, section):
    # Create masks
    t_mask = template > 0
    s_mask = section > 0
    # Return ratio of overlapping segments
    return sum(sum(np.logical_and(t_mask, s_mask))) / sum(sum(t_mask))


def find_average_diff(spec_a, spec_b):
    diff = abs(spec_a - spec_b)
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
    sim = np.ones(template.shape) - diff
    # Return average similarity
    return sum(sum(sim)) / (len(sim) * len(sim[0]))


# Get user parameters
file_dir = input("Enter the relative path of the file for searching: ")

# Load audio data for comparison
print("Loading audio data for searching")
sr, stereo_samples = wavfile.read(file_dir)
mono_samples = np.array(stereo_samples)
mono_samples = mono_samples.transpose()
mono_samples = ((mono_samples[0] + mono_samples[1]) / 2)
audio_len = len(mono_samples) / sr
# Create spectrogram, or load if already created for this audio file
np_dir = file_dir.replace('.wav', '.npy')
if not os.path.exists(np_dir):
    frequencies, times, spectrogram = signal.spectrogram(mono_samples, sr, nperseg=512, noverlap=384)
    np_spectrogram = np.array(spectrogram)
    np_spectrogram = np.log(np_spectrogram)
    np_spectrogram = np.clip(np_spectrogram, -2, 3)
    np_spectrogram = np.flipud(np_spectrogram)
    # Cut off low frequencies (under 1k) (first 10)
    np_spectrogram = np.delete(np_spectrogram, slice(1, 10), 0)
    np_frequencies = np.array(frequencies)
    np_frequencies = np.delete(np_frequencies, slice(1, 10), 0)
    # Transpose so X axis is time
    np_spectrogram = np_spectrogram.transpose()
else:
    np_spectrogram = np.load(np_dir)
print("Audio data loaded")
np.save(np_dir, np_spectrogram)

# Load song_type data
songs_specs = []
for song_type in range(0, 23):
    # Load song templates
    spec_dir = 'specs/' + str(song_type)
    specs = []
    print("Loading spectrograms for", song_type)
    for filename in os.listdir(spec_dir):
        path = spec_dir + "/" + filename
        specs.append(np.load(path))
    print("Loaded", len(specs), "spectrograms")
    songs_specs.append(specs)

# Iterate through entire spectrogram, creating array of similarities
print("Generating matches map for audio data based on songs")
probabilities = [[] for i in range(0, 23)]
# This represents the likelihood (value) of a segment being of a certain song type (y) at a given time (x)
song_spec_len = len(songs_specs[0][0])
print(np_spectrogram.shape)
for starting_point in range(0, len(np_spectrogram) - song_spec_len, 16):
    # Find average similarity to each song
    comparison_spec = np_spectrogram[starting_point:starting_point + song_spec_len]
    for song_type in range(0, 23):
        song_spec = songs_specs[song_type][0]
        similarity = find_mask_sim(song_spec, comparison_spec)
        # Add similarity of audio to the song at this instance
        probabilities[song_type].append(similarity)
# Save probabilities
np.save(np_dir.replace('data', 'matches'), probabilities)
print("Saved probabilities")
