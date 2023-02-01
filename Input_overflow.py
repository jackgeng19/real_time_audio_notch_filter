import pyaudio
import numpy as np
from scipy.signal import iirnotch, lfilter

# Define the desired notch filter parameters
freq = 4400  # The frequency to notch out
q = 5  # The Q-factor of the filter

p = pyaudio.PyAudio()

info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

# Select device by name
devicename = "MacBook Air扬声器"
device_index = None
for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('name') == devicename):
        device_index = i
        break

if device_index is None:
    raise ValueError("Device not found")

# Design the notch filter
b, a = iirnotch(freq, q, 44100)

# Open the audio input and output devices using PyAudio
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                output=True,
                output_device_index=device_index,
                frames_per_buffer=4410)

stop_flag = False
while not stop_flag:
    # Read a chunk of audio data from the input stream
    data = stream.read(4410, exception_on_overflow = False)
    audio_data = np.frombuffer(data, dtype=np.int16)
    # Apply the notch filter to the audio data
    filtered_audio = lfilter(b, a, audio_data)
    # Write the filtered audio data to the output stream
    stream.write(filtered_audio.tobytes())
