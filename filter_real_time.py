import pyaudio
import numpy

sample_rate: int = 44011 #Hz
quality: int = 30

f_notch: int = 100 #Hz

p = pyaudio.PyAudio()