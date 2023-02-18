using NAudio.Wave;

public class AudioEqualizer
{
    private readonly Equalizer equalizer;

    public AudioEqualizer()
    {
        equalizer = new Equalizer();
        equalizer.SampleRate = 44100;
        equalizer.Bandwidth = 2.0f;
        equalizer.Bands = new[]
        {
            new EqualizerBand { Frequency = 32, Gain = 0 },
            new EqualizerBand { Frequency = 64, Gain = 0 },
            new EqualizerBand { Frequency = 125, Gain = 0 },
            new EqualizerBand { Frequency = 250, Gain = 0 },
            new EqualizerBand { Frequency = 500, Gain = -12 }, // Cut off 440Hz
            new EqualizerBand { Frequency = 1000, Gain = 0 },
            new EqualizerBand { Frequency = 2000, Gain = 0 },
            new EqualizerBand { Frequency = 4000, Gain = 0 },
            new EqualizerBand { Frequency = 8000, Gain = 0 },
            new EqualizerBand { Frequency = 16000, Gain = 0 }
        };
    }

    public void SetGain(int bandIndex, float gain)
    {
        if (bandIndex < 0 || bandIndex >= equalizer.Bands.Length)
        {
            throw new ArgumentOutOfRangeException("bandIndex");
        }

        equalizer.Bands[bandIndex].Gain = gain;
    }

    public float[] Process(WaveStream input)
    {
        var sampleProvider = new SoundTouchWaveProvider(input);
        var sampleBuffer = new float[sampleProvider.WaveFormat.SampleRate * sampleProvider.WaveFormat.Channels];
        int bytesRead;
        var outputBuffer = new float[sampleBuffer.Length];
        var output = new List<float>();

        while ((bytesRead = sampleProvider.Read(sampleBuffer, 0, sampleBuffer.Length)) > 0)
        {
            for (int i = 0; i < bytesRead / sizeof(float); i++)
            {
                sampleBuffer[i] = equalizer.Transform(sampleBuffer[i]);
            }

            outputBuffer = sampleBuffer;
            output.AddRange(outputBuffer.Take(bytesRead / sizeof(float)));
        }

        return output.ToArray();
    }
}
