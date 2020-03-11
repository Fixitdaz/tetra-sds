import numpy as np
import wavio
# Parameters
rate = 44100    # samples per second
T = 3           # sample duration (seconds)
f = 440.0       # sound frequency (Hz)
# Compute waveform samples
t = np.linspace(0, T, T*rate, endpoint=False)
x = np.sin(2*np.pi * f * t)

print(type(x))
# Write the samples to a file
wavio.write("sine.wav", x, rate, sampwidth=3)