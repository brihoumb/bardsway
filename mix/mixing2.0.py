import os
import sys
import pydub
from pydub import AudioSegment
import wave
import contextlib
import soundfile
import subprocess

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
    newAudio.set_frame_rate(24)
    newAudio.export(output, format="wav")

def accompaniment(patern, the_files):
    file_names = the_files
    for x in file_names:
        if (x.find("VOX") > -1):
            file_names.remove(x)
            x = 0
    for x in file_names:
        if (x.find("Vox") > -1):
            file_names.remove(x)
            x = 0
    for x in file_names:
        if (x.find("Vocal") > -1):
            file_names.remove(x)
            x = 0
    if (file_names == []):
      print ("No enough file to mix accompaniment.wav")  
    elif (file_names[len(file_names) - 1].find("Vox") > -1 or file_names[len(file_names) - 1].find("VOX") > -1 or file_names[len(file_names) - 1].find("Vocal") > -1):
        file_names.remove(file_names[len(file_names) - 1])
    return (file_names)

def other(patern, file_names):
    i = 0
    j =	0
    y =	0
    file_to_mix = []
    if (len(patern) > 1):
        for x in file_names:
            if (file_names[i].find(patern[j],0,len(file_names[i])) == -1):
                file_to_mix.insert(y, file_names[i])
                y = y + 1
            i = i + 1
        i = 0
        j = 1
        while (j < len(patern)):
            i = 0
            for x in file_to_mix:
                if (x.find(patern[j],0,len(x)) > -1):
                    file_to_mix.remove(x)
                    x = 0
                    j = 0
                    i = -1
                i = i + 1
            j = j + 1
        print (file_to_mix)
        return (file_to_mix)

def patern_finder(argv):
    patern = []
    i = 2
    y = 0
    while (i < len(argv) - 1):
        patern.insert(y, argv[i])
        y = y + 1
        i = i + 1
    return (patern)

def multiple_wav_cut(wavlenght, path, output, wav_nbr, combined):
    i = 0
    div = 2
    if (output == "mixture"):
        while (i < wav_nbr):
            cutwav((wavlenght/div), ((wavlenght/div) + 7), (path + output.lower() + '.wav'), (path + output.lower() + str(i) + '.wav'))
            combined.export(path + "linear_" + output.lower() + str(i) +  ".wav", format='wav')
            div += 1
            i += 1
    else:
        while (i < wav_nbr): 
            cutwav((wavlenght/div), ((wavlenght/div) + 7), (path + output.lower() + '.wav'), (path + output.lower() + str(i) + '.wav'))
            div += 1
            i += 1

def mix(file_to_mix, output, patern, file_names, path, wav_nbr):
    i = 0
    if (file_to_mix == []):
        print ("No enough file to mix for " + output)
    elif (patern == ""):
        combined = AudioSegment.from_file(relevant_path + file_to_mix[0])
        print ("Mixing : " + file_to_mix[0])
        for x in file_to_mix:
            if (i != 0):
                if (x.find("other") == -1 or x.find("accompaniment") == -1):
                    combined = combined.overlay(AudioSegment.from_file(relevant_path + x))
                    print("Mixing : " + x)
            i = i + 1
        print ("export ==> " + output + ".wav")
        combined.export(path + output.lower() + ".wav", format='wav')
        wavlenght = wavlen(path + output.lower() + '.wav')
        if (wav_nbr == 1):
            cutwav((wavlenght/2), ((wavlenght/2) + 7), (path + output.lower() + '.wav'), (path + output.lower() + '.wav'))
            if (output == "mixture"):
                combined.export(path + "linear_" + output.lower() + ".wav", format='wav')
        else:
            multiple_wav_cut(wavlenght, path, output, wav_nbr, combined)

    else:
        i = 0
        while (i < len(patern)):
            if (i != -1):
                y = 0
                j = 0
                file_to_mix = []
                for x in file_names:
                    if (file_names[j].find(patern[i],0,len(file_names[j])) >= 0):
                        file_to_mix.insert(y, file_names[j])
                        print ("wll mix " + patern[i] + ".wav :" + file_names[j])
                        y = y + 1
                    j = j + 1
                print ("xil mix  patern === " + patern[i])
                print (file_to_mix)
                mix(file_to_mix, str(patern[i]), "" , file_names, path, wav_nbr)
            i = i + 1


def convert(file_names, pcm):
    for x in file_names:
        data, samplerate = soundfile.read(x)
        print("converting " + x)
        soundfile.write(x, data, samplerate, subtype=pcm)

if (len(sys.argv) < 4):
    print ("Usage: python mixing2.0.py [File path to mix][patern to find][cutwav_nbr]")
    exit (0)

wav_nbr = int(sys.argv[len(sys.argv) - 1])
mixed_files = []
relevant_path = sys.argv[1]
file_to_mix = []
included_extensions = ['wav']
file_names = [fn for fn in os.listdir(relevant_path)
              if any(fn.endswith(ext) for ext in included_extensions)]
patern = patern_finder(sys.argv)
mix(other(patern, file_names), "other", "", sys.argv, relevant_path, wav_nbr)
mix(accompaniment(patern, file_names), "accompaniment", "", sys.argv, relevant_path, wav_nbr)
file_names = [fn for fn in os.listdir(relevant_path)
              if any(fn.endswith(ext) for ext in included_extensions)]
mix(file_names, "mixture", "", file_names, relevant_path, wav_nbr)
i = 0
y = 0
for x in file_names:
    if (file_names[i].find(sys.argv[2],0,len(file_names[i])) >= 0):
        file_to_mix.insert(y, file_names[i])
        y = y + 1
    i = i + 1
if (len(file_to_mix) == 1):
    exit (0)
print (file_to_mix)
if (len(sys.argv) > 4):
    mix(file_to_mix, sys.argv[len(sys.argv) - 1], patern, file_names, relevant_path, wav_nbr)
else:
    mix(file_to_mix, sys.argv[3], "", file_names, relevant_path, wav_nbr)
subprocess.Popen(['notify-send', "Mix Done"])
print ("\a")
