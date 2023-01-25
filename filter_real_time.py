import pyaudio
import numpy as np
from scipy.signal import notch_filter

# Define the parameters of the filter
sample_rate: int = 44011 #Hz
quality: int = 30
f_notch: int = 1000 #Hz

# Open an input and output stream using PyAudio
p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paFloat32, channels = 1, rate = sample_rate, input = True, output = True)

# Loop to apply the filter to the audio data in real-time
while True:
    # Read audio data from the input stream
    data = stream.read(1024)
    audio_data = np.fromstring(data, dtype=np.float32)

    # Apply the notch filter to the audio data
    filtered_data = notch_filter(audio_data, f_notch, quality, sample_rate)

    # Write the filtered audio data to the output stream
    stream.write(filtered_data.tostring())

# Close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()