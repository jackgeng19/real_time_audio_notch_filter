import pyaudio

# Request for audio input and output device and its index

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

# for i in range(0, numdevices):
#     print(p.get_device_info_by_host_api_device_index(0, i).get('name'))

device_info = p.get_host_api_info_by_index(0)['deviceCount']
for i in range(device_info):
    device = p.get_device_info_by_host_api_device_index(0, i)
    print("Device %d: %s" % (i, device['name']))