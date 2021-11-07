import sys
import csv
import os
import wave
import contextlib
import string

def getduration(x, path, d):

    if (x.find(d) != -1):
        print ('finded !!!')
        print (x.find(d))
        
        x = x[x.find(d) + len(d):]
    print ('path ==> ' + path)
    fname = path + x
    print ('getduration ==> x == ' + fname)
    relevant_path = fname
    included_extensions = ['wav']
    files = [fn for fn in os.listdir(relevant_path)
              if any(fn.endswith(ext) for ext in included_extensions)]
    i = 0
    j = 0
    while (i != 1):
        if (files[j] != 'other.wav' and files[j] != 'accompaniment.wav' and files[j] != 'drum.wav' and files[j] != 'bass.wav' and files[j] != 'guitar.wav' and files[j] != 'mixture.wav' and files[j] != 'linear_mixture.wav' and files[j] != 'vocals.wav'):
            i = 1
            fname += '/' + files[j]
        j += 1
#    files = [os.path.join(fname, o) for o in os.listdir(fname)
#                    if os.path.isdir(os.path.join(fname,o))]
    print (files)
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        print(duration)
    return (duration)

if (len(sys.argv) < 5):
    print ("Usage : python trainmodelgenerator.py [path to dataset][path to compare dataset][output_train.csv][output_validation.csv]")
    exit (0)

d = sys.argv[1]
files = [os.path.join(d, o) for o in os.listdir(d)
                    if os.path.isdir(os.path.join(d,o))]
g = sys.argv[2]
files_comp = [os.path.join(g, o) for o in os.listdir(g)
                    if os.path.isdir(os.path.join(g,o))]

print (files)
tmp = 1
text = []
newline = '\n'
first_line = 'mix_path,vocals_path,drums_path,bass_path,guitar_path,other_path,duration'
text.insert(0, first_line)
for x in files:
    duration = str(getduration(x, g, d))
    duration = duration[0:10]
    text.insert(tmp, x + '/mixture.wav,'+ x + '/vocals.wav,'+ x + '/drum.wav,'+ x + '/bass.wav,'+ x + '/guitar.wav,'+ x + '/other.wav,'+ duration)
    tmp += 1
    print ("len tmp ====>")
    print (tmp)
tmp = 0
with open(sys.argv[3],'wb') as file:
    for line in text:
        if (tmp >= ((len(text)/5) * 4)):
            break
        file.write(line.encode())
        file.write(newline.encode())
        tmp += 1
tmp = 0
with open(sys.argv[4],'wb') as file:
    file.write(first_line.encode())
    file.write(newline.encode())
    for line in text:
        if (tmp >= ((len(text)/5) * 4)):
            file.write(line.encode())
            file.write(newline.encode())
        tmp += 1

"""    with open(sys.argv[3], 'w', newline='\n') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if (tmp == 0):
            print ("bzaaaaaaaaaaaaaaaaaaaaa")
            csvwriter.writerow(['mix_path','vocals_path','drums_path','bass_path','guitar_path','other_path','duration'])
            tmp = 1
#        csvwriter.writerow([x + '/mixture.wav', x + '/vocals.wav', x + '/drum.wav', x + '/bass.wav', x + '/guitar.wav', x + '/other.wav', getduration(x, g, d)])

"""
"""tmp = 0

for x in files_comp:
    for y in files:
        if (x == y):
            tmp = 1
    if (tmp == 1):
        files_comp.remove(x)
        tmp = 0
        x = -1
    
file_to_convert = []
for x in files:
    file_to_convert.insert(0, x + '/other.wav')
    file_to_convert.insert(0, x + '/vocals.wav')
    file_to_convert.insert(0, x + '/accompaniment.wav')
    file_to_convert.insert(0, x + '/guitar.wav')
    file_to_convert.insert(0, x + '/drum.wav')
    file_to_convert.insert(0, x + '/bass.wav')
    file_to_convert.insert(0, x + '/mixture.wav')
    file_to_convert.insert(0, x + '/linear_mixture.wav')
"""
