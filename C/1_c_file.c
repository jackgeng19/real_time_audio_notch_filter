#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <portaudio.h>

#define SAMPLE_RATE (44100)
#define FRAMES_PER_BUFFER (512)

typedef struct {
    double frequency;
    double gain;
    double delay_buffer[1024];
    int write_index;
} CombFilter;

void init_comb_filter(CombFilter *filter, double frequency, double gain)
{
    filter->frequency = frequency;
    filter->gain = gain;
    filter->write_index = 0;

    int delay_samples = round((double)SAMPLE_RATE / filter->frequency);
    int delay_buffer_size = delay_samples * 2;

    for (int i = 0; i < delay_buffer_size; i++) {
        filter->delay_buffer[i] = 0.0;
    }
}

void apply_comb_filter(CombFilter *filter, double *input, double *output)
{
    for (int i = 0; i < FRAMES_PER_BUFFER; i++) {
        double input_sample = input[i];
        double delay_sample = filter->delay_buffer[filter->write_index];
        double output_sample = input_sample - filter->gain * delay_sample;

        filter->delay_buffer[filter->write_index] = input_sample + filter->gain * output_sample;

        output[i] = output_sample;
        filter->write_index = (filter->write_index + 1) % (int)(2 * round((double)SAMPLE_RATE / filter->frequency));
    }
}

static int audio_callback(const void *input_buffer, void *output_buffer, unsigned long frames_per_buffer, const PaStreamCallbackTimeInfo *time_info, PaStreamCallbackFlags status_flags, void *user_data)
{
    CombFilter *filter = (CombFilter *)user_data;
    double *input = (double *)input_buffer;
    double *output = (double *)output_buffer;

    apply_comb_filter(filter, input, output);

    return paContinue;
}

int main(void)
{
    PaStream *stream;
    PaError err;
    CombFilter filter;
    double frequency = 1000.0;
    double gain = 0.5;

    err = Pa_Initialize();
    if (err != paNoError) {
        printf("Error: Failed to initialize PortAudio.\n");
        return 1;
    }

    init_comb_filter(&filter, frequency, gain);

    err = Pa_OpenDefaultStream(&stream, 1, 1, paFloat32, SAMPLE_RATE, FRAMES_PER_BUFFER, audio_callback, &filter);
    if (err != paNoError) {
        printf("Error: Failed to open PortAudio stream.\n");
        return 1;
    }

    err = Pa_StartStream(stream);
    if (err != paNoError) {
        printf("Error: Failed to start PortAudio stream.\n");
        return 1;
    }

    printf("Press enter to stop...\n");
    getchar();

    err = Pa_StopStream(stream);
    if (err != paNoError) {
        printf("Error: Failed to stop PortAudio stream.\n");
        return 1;
    }

    err = Pa_CloseStream(stream);
    if (err != paNoError) {
        printf("Error: Failed to close PortAudio stream.\n");
        return 1;
    }

    err = Pa_Terminate();
    if (err != paNoError) {
        printf("Error: Failed to terminate PortAudio.\n");
				return 1;
		}
		return 0;
}