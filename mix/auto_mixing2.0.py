import sys
import os

if (len(sys.argv) < 2):
    print ("Usage : python auto_mixing2.py [path/to/main/directory]")
    exit (0)
d = sys.argv[1]
files = [os.path.join(d, o) for o in os.listdir(d) 
                    if os.path.isdir(os.path.join(d,o))]
i = 0
j = 0
while (i < len(files)):
    while(j < len(files[i])):
        if (files[i] == ' ' or files[i] == '\'' or files[i] == '\"'):
            files[i] = files[i][:j] + '\\' + files[i][j:]
        j += 1
    i += 1
print(files)
for x in files:
    #os.system('python mixing2.0.py ./' + x + '/ Drum Bass Gtr Vox 1')
    os.system('python stemmp4creator.py mp4datasetimg.png ../final_dataset/' + x + '/mixture.wav  ../final_dataset/' + x + '.stems.mp4')
os.system('python convert.py ./ PCM_16')
