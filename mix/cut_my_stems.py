from pydub import AudioSegment
import wave
import sys
import contextlib
import os

def wavlen(wavfile):
    fname = wavfile
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return (duration)

def cutwav(t1, t2, wavfile, output):
    t1 = t1 * 1000 #Works in milliseconds
    t2 = t2 * 1000
    newAudio = AudioSegment.from_wav(wavfile)
    newAudio = newAudio[t1:t2]
    newAudio.export(output, format="wav")


if (len(sys.argv) < 3):
    print ("Usage : cut_my_stems.py path/to/folder path/to/copy")
relevant_path = sys.argv[1]
path = sys.argv[2]
file_to_mix = []
included_extensions = ['wav']
file_names = [fn for fn in os.listdir(relevant_path)
              if any(fn.endswith(ext) for ext in included_extensions)]
for x in file_names:
    wavlenght = wavlen(relevant_path + x)
    cutwav((wavlenght/2), ((wavlenght/2) + 7), (relevant_path + x), path + x)
