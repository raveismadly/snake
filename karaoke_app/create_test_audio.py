


import numpy as np
from scipy.io.wavfile import write

# Parameters
sample_rate = 44100  # Hz
duration = 5.0       # seconds

# Create a simple sine wave
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
frequency = 440  # A4 note
waveform = 0.5 * np.sin(2 * np.pi * frequency * t)

# Convert to 16-bit PCM
waveform_int16 = np.int16(waveform * 32767)

# Save to WAV file
filename = 'test_audio.wav'
write(filename, sample_rate, waveform_int16)
print(f"Created test audio file: {filename}")

