import ffmpeg
import sys
import os






if (len(sys.argv) < 4):
    print ("Usage: python stemmp4creator.py [image path][input.wav][output.stem.mp4]")
    exit (0)
os.system('ffmpeg -loop 1 -i ' + sys.argv[1] + ' -i ' + sys.argv[2] + ' -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest ' + sys.argv[3])
"""
This will mix an image with a wavfile to create a mp4 file
"""
"""    
input_still = ffmpeg.input(sys.argv[1])
input_audio = ffmpeg.input(sys.argv[2])

(
    ffmpeg
    .concat(input_still, input_audio, v=1, a=1)
    .output(sys.argv[3])
    .run(overwrite_output=True)
)
"""
