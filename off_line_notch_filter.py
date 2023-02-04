__author__ = "Jack Qicheng Geng"

import soundfile as sf
import scipy.signal
import numpy as np
import tkinter as tk
from tkinter import filedialog

def apply_filter():
    # Ask the user the input file's dir
    file_path = filedialog.askopenfilename()

    # Ask the user to get center frequency and bandwidth
    center_frequency = float(center_frequency_entry.get())
    bandwidth = float(bandwidth_entry.get())

    # Read the audio file
    data, sr = sf.read(file_path)

    # Define the notch filter parameters in Hz
    center_frequency = center_frequency 
    bandwidth = bandwidth

    # Create the notch filter we want
    # Question remain: what is the difference between iirnotch and notch in scipy.signal
    b, a = scipy.signal.iirnotch(center_frequency, bandwidth, sr)

    # Apply the filter to the audio that is transferred
    i = 1
    m = center_frequency
    filtered_data = scipy.signal.lfilter(b, a, data)
    while i < 62:
        b, a = scipy.signal.iirnotch(m, bandwidth, sr)
        filtered_data = scipy.signal.lfilter(b, a, filtered_data)
        m -= 1
        i += 1

    # Write the filtered wav to a new file
    sf.write('filtered_file.wav', filtered_data, sr)
    label_result.config(text='File filtered successfully')

# Use tkinter to create the main window
root = tk.Tk()
root.title("Notch Filter")

# Create input fields for center frequency and bandwidth
center_frequency_label = tk.Label(root, text="Center frequency (Hz)")
center_frequency_label.pack()
center_frequency_entry = tk.Entry(root)
center_frequency_entry.pack()

bandwidth_label = tk.Label(root, text="Bandwidth (Hz)")
bandwidth_label.pack()
bandwidth_entry = tk.Entry(root)
bandwidth_entry.pack()

# Create a button to apply the filter by calling the def apply_filter
apply_filter_button = tk.Button(root, text="Apply Filter", command=apply_filter)
apply_filter_button.pack()

# Create a label to show the result
label_result = tk.Label(root, text="")
label_result.pack()

# Run the GUI
root.mainloop()