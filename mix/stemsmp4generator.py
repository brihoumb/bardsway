import sys
import os


if (len(sys.argv) < 4):
    print ("Usage: python stemmp4creator.py [image path][input.wav][output.stem.mp4]")
    exit (0)
d = './'
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
    os.system('ffmpeg -loop 1 -i ' + sys.argv[1] + ' -i \'' + x + '/mixture.wav\' -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest \'' + x + '.stem.mp4\'')
