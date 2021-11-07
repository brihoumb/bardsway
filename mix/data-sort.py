import sys
import os
from shutil import copytree



def dataset_folder_generator(folders):

    access_rights = 0o755
    for path in folders:
        try:
            os.mkdir(path, access_rights)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s" % path)

def copy_files(src, dest):
    try:
        copytree(src, dest)    
    except FileExistsError:
        print ("The directory : %s already exist" % dest)
    else:
        print ("Succesfully copy the directory " +  src  + " to " + dest)
        
if (len(sys.argv) < 2):
    print ("Usage : data-sort.py [path/to/main/folder]")
    exit (0)

folders = ["./01_Drum_Bass_Gtr_Vox", "./02_Drum_Bass_Sax_Vox", "./03_Drum_Bass_Gtr_Sax_Vox", "./04_Drum_Bass_Trumpet_Vox", "./05_Drum_bass_Trumpet_Gtr_Vox", "./06_to_check", "./07_no_vocals"]
dataset_folder_generator(folders)

d = sys.argv[1]
drumct = 0
bassct = 0
voxct = 0
gtrct = 0
saxct = 0
trumpetct = 0
count = 0
files = [os.path.join(d, o) for o in os.listdir(d)
                    if os.path.isdir(os.path.join(d,o))]
included_extensions = ['wav']
not_mixable = []
for relevant_path in files:
    if (any(relevant_path in x for x in folders) == False):
        file_names = [fn for fn in os.listdir(relevant_path)
                      if any(fn.endswith(ext) for ext in included_extensions)]
        print ("In : " + relevant_path)
        print ("Before Count ==>  " + str(count))
        for x in file_names:
            if (x.find("Drum") != -1 or x.find("DRUM") != -1 or x.find("drum") != -1):
                drumct = 1
            if (x.find("Bass") != -1 or x.find("BASS") != -1 or x.find("bass") != -1):
                bassct = 1
            if (x.find("Gtr") != -1 or x.find("Guitar") != -1 or x.find("GUITAR") != -1 or x.find("GTR") != -1):
                gtrct = 5
            if (x.find("Vox") != -1 or x.find("VOX") != -1 or x.find("vox") != -1 or x.find("Vocal") != -1 or x.find("VOCAL") != -1):
                voxct = 1
            if (x.find("Sax") != -1 or x.find("SAX") != -1 or x.find("sax") != -1):
                saxct = 10
            if (x.find("Trumpet") != -1 or x.find("TRUMPET") != -1 or x.find("trumpet") != -1):
                trumpetct = 100
            if (x.find("Loop") != -1 or x.find("LOOP") != -1):
                drumct = 1000
        count = saxct + drumct + bassct + voxct + gtrct
        print ("Count ==>  " + str(count))
        if (count == 8):
            print ("Copy of : " + relevant_path + "in ./01_Drum_Bass_Gtr_Vox")
            print( "./01_Drum_Bass_Gtr_Vox" + relevant_path[1:])
            copy_files(relevant_path, "./01_Drum_Bass_Gtr_Vox" + relevant_path[1:])
            print ("Drum bass guitar vox")
        elif (count == 13):
            print ("Copy of : " + relevant_path + "in ./02_Drum_Bass_Sax_Vox")
            copy_files(relevant_path, "./02_Drum_Bass_Sax_Vox" + relevant_path[1:])
        elif (count == 18):
            print ("Copy of : " + relevant_path + "in ./03_Drum_Bass_Gtr_Sax_Vox")
            copy_files(relevant_path, "./03_Drum_Bass_Gtr_Sax_Vox" + relevant_path[1:])
        elif (count == 103):
            print ("Copy of : " + relevant_path + "in ./04_Drum_Bass_Trumpet_Vox")
            copy_files(relevant_path, "./04_Drum_Bass_Trumpet_Vox" + relevant_path[1:])
        elif (count == 108):
            print ("Copy of : " + relevant_path + "in ./05_Drum_Bass_Gtr_Trumpet_Vox")
            copy_files(relevant_path, "./05_Drum_Bass_Gtr_Trumpet_Vox" + relevant_path[1:])
        elif ((count < 8 or count > 118) or count == 11 or count == 12):
            if (voxct != 1):
                print ("Copy of : " + relevant_path + "in ./07_no_vocals")
                copy_files(relevant_path, "./07_no_vocals" + relevant_path[1:])
                print ("Not mixable !!!!!!!!!!!!!!!!!!!!!!!")
            else:
                print ("Copy of : " + relevant_path + "in ./06_to_check")
                copy_files(relevant_path, "./06_to_check" + relevant_path[1:])
                not_mixable.insert(0, relevant_path)
        drumct = 0
        bassct = 0
        gtrct = 0
        voxct = 0
        saxct = 0
        trumpetct = 0
        count = 0
if (len(not_mixable) > 0):
    print ("the following files had been copy in ./06_to_check :")
    for x in not_mixable:
        print (x)
