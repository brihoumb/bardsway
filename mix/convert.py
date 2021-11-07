import sys
import os
import soundfile

if (len(sys.argv) < 3):
    print ("Usage : python convert.py [path/to/main/file][pcm (PCM_16/PCM_24/PCM_32)]")
    exit (0)

import wave, array

def make_stereo(file1, output):
    ifile = wave.open(file1)
    print (ifile.getparams())
    # (1, 2, 44100, 2013900, 'NONE', 'not compressed')
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = ifile.getparams()
    assert comptype == 'NONE'  # Compressed not supported yet
    array_type = {1:'B', 2: 'h', 4: 'l'}[sampwidth]
    left_channel = array.array(array_type, ifile.readframes(nframes))[::nchannels]
    ifile.close()

    stereo = 2 * left_channel
    stereo[0::2] = stereo[1::2] = left_channel

    ofile = wave.open(output, 'w')
    ofile.setparams((2, sampwidth, framerate, nframes, comptype, compname))
    ofile.writeframes(stereo.tostring())
    ofile.close()


def convert(file_names, pcm):
    print (file_names)
    data, samplerate = soundfile.read(file_names)
    print("converting " + x)
    soundfile.write(file_names, data, samplerate, subtype=pcm)

pcm = sys.argv[2]
d = sys.argv[1]
files = [os.path.join(d, o) for o in os.listdir(d)
                    if os.path.isdir(os.path.join(d,o))]
print (files)
file_to_convert = []
for x in files:
    file_to_convert.insert(0, x + '/other.wav')
    file_to_convert.insert(0, x + '/vox.wav')
    file_to_convert.insert(0, x + '/accompaniment.wav')
    file_to_convert.insert(0, x + '/gtr.wav')
    file_to_convert.insert(0, x + '/drum.wav')
    file_to_convert.insert(0, x + '/bass.wav')
    file_to_convert.insert(0, x + '/mixture.wav')
    file_to_convert.insert(0, x + '/linear_mixture.wav')

for x in file_to_convert:
    convert(x, pcm)
    make_stereo(x, x)
