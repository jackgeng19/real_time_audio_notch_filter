import pyaudio
import numpy as np
from scipy.signal import iirnotch, lfilter
import keyboard

# Define the parameters of the filter
sample_rate: int = 4800 #Hz
quality: int = 35
f_notch: int = 1000 #Hz

# Make the filter first
b, a = iirnotch(f_notch, quality, sample_rate)

# Open an input and output stream using PyAudio
p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paFloat32, channels = 1, rate = sample_rate, input = True, output = True, frames_per_buffer = 1024)

# Loop to apply the filter to the audio data in real-time
while True:
    if keyboard.is_pressed('space'):  # if the space is pressed
        break  # break out of the loop
    # Read audio data from the input stream
    data = stream.read(1024)
    # Converts data to be readable by lfilter
    audio_data = np.frombuffer(data, dtype=np.float32)

    # Apply the filter made previously to the audio data
    filtered_data = lfilter(b, a, audio_data)

    # Write the filtered audio data to the output stream
    stream.write(filtered_data.tostring())

# Close the stream
stream.stop_stream()
stream.close()
p.terminate()