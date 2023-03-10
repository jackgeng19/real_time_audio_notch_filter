from __future__ import division
import pyaudio
import scipy.signal
import numpy as np
from six.moves import queue

# Inspired by STT model from Google Cloud service

# Audio recording parameters
RATE = 48000  # or 8000
CHUNK = int(RATE / 10)  # 100ms - control the length


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        # Implement Python Audio Stream Interaface
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)


def output_audio_data(freq, quality, audio_data_generator):
    """Outputs the audio data from the generator through the speaker."""
    audio_interface = pyaudio.PyAudio()
    stream = audio_interface.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        output=True,
        frames_per_buffer=CHUNK,
    )
    for audio_data in audio_data_generator:
        ## Uncomment this to apply the filter
        # audio_data = np.frombuffer(audio_data, dtype = np.uint32) #convert to one-dimension array
        # b, a = scipy.signal.iirnotch(freq, quality, RATE) 
        # audio_data = scipy.signal.lfilter(b, a, audio_data)
        stream.write(audio_data)
    stream.stop_stream()
    stream.close()
    audio_interface.terminate()

# Use the MicrophoneStream to get audio data generator
def main():
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        output_audio_data(440, 100, audio_generator)

if __name__ == "__main__":
    main()