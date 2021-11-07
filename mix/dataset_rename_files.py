import sys
import os

if (len(sys.argv) < 2):
    print ("Usage : dataset_rename_files.py [path/to/main/folder]")
    exit (0)

d = sys.argv[1]
files = [os.path.join(d, o) for o in os.listdir(d)
                    if os.path.isdir(os.path.join(d,o))]
included_extensions = ['wav']
for relevant_path in files:
    file_names = [fn for fn in os.listdir(relevant_path)
                  if any(fn.endswith(ext) for ext in included_extensions)]
    for x in file_names:
        if ((x.find("Hat") != -1 or x.find("Snare") != -1 or x.find("Kick") != -1 or x.find("Tom") != -1 or x.find("Cymbal") != -1 or x.find("HiHat") != -1 or x.find("Ride") != -1) and x.find("Drum") != 0):
            os.rename(relevant_path + "/"  + x, relevant_path +"/Drum"+x)
            print (relevant_path + "/" + x +" Succesfuly renamed")
        elif (x.find("Over") != -1 or x.find("Room") != -1 or x.find("OVER") != -1 or x.find("ROOM") != -1):
            print (relevant_path + '/' + x + " Succesfully removed")
            os.remove(relevant_path + '/' + x)
        elif ((x.find("Vocal") != -1 or x.find("vocal") != -1) and x.find("Vox") < 0):
            os.rename(relevant_path + "/" + x, relevant_path + "/Vox" + x)
