import os
import sys
import shutil

if (len(sys.argv) < 2):
    print ("Usage : [Main Directory][Path to copy][nbr of copy (optional*)])")
    exit (0)
path = sys.argv[1]
final_path = sys.argv[2]
directory = []
for o in os.listdir(path):
    if (o.find('.py') == -1 and o.find('.wav') == -1):
        print ('will create : ' + o + ' to ' + final_path + o)
        directory.insert(0, o)
        print (directory)
        print ("o =========> ")
        print (o)

        try:
            os.mkdir(final_path + o)
        except OSError:
            print ("Creation of the directory %s failed" % final_path + o)
        else:
            print ("Successfully created the directory %s " % final_path + o)

for x in directory:
    print ('Copy of ' + x + 'directory : in progress 0%\r', end='\r')
    shutil.copy(path + x + '/drum.wav', final_path + x + '/drum.wav')
    print ('Copy of ' + x + 'directory : in progress 15%\r', end='\r')
    shutil.copy(path + x + '/gtr.wav', final_path + x + '/guitar.wav')
    print ('Copy of ' + x + 'directory : in progress 30%\r', end='\r')
    shutil.copy(path + x + '/bass.wav', final_path + x + '/bass.wav')
    print ('Copy of ' + x + 'directory : in progress 45%\r', end='\r')
    shutil.copy(path + x + '/vox.wav', final_path + x + '/vocals.wav')
    print ('Copy of ' + x + 'directory : in progress 60%\r', end='\r')
    shutil.copy(path + x + '/accompaniment.wav', final_path + x + '/accompaniment.wav')
    print ('Copy of ' + x + 'directory : in progress 75%\r', end='\r')
    shutil.copy(path + x + '/mixture.wav', final_path + x + '/mixture.wav')
    print ('Copy of ' + x + 'directory : in progress 90%\r', end='\r')
    shutil.copy(path + x + '/linear_mixture.wav', final_path + x + '/linear_mixture.wav')
    print ('Copy of ' + x + 'directory : in progress 95%\r', end='\r')
    shutil.copy(path + x + '/other.wav', final_path + x + '/other.wav')
    print ('Copy of ' + x + 'directory : in progress 100%')
    print (x + ' directory : done')

if (len(sys.argv) > 3):
    i = 0
    nbr_wav = int(sys.argv[3])
    while (i < nbr_wav):
        directory = []
        for o in os.listdir(path):
            if (o.find('.wav') == -1 and o.find('.py') == -1):
                print ('will create : ' + o + ' to ' + final_path + o + str(i))
                directory.insert(0, o + str(i))
                print (directory)
                try:
                    os.mkdir(final_path + o + str(i))
                except OSError:
                    print ("Creation of the directory %s failed" % final_path + o + str(i))
                else:
                    print ("Successfully created the directory %s " % final_path + o + str(i))
        for x in directory:                                                                      
            print ('Copy of ' + x + 'directory : in progress 0%\r', end='\r')                    
            shutil.copy(path + x + '/drum' + str(i) + '.wav', final_path + x + '/drum.wav')                    
            print ('Copy of ' + x + 'directory : in progress 15%\r', end='\r')                   
            shutil.copy(path + x + '/gtr' + str(i) + '.wav', final_path + x + '/guitar.wav')                   
            print ('Copy of ' + x + 'directory : in progress 30%\r', end='\r')                   
            shutil.copy(path + x + '/bass' + str(i) + '.wav', final_path + x + '/bass.wav')                    
            print ('Copy of ' + x + 'directory : in progress 45%\r', end='\r')                   
            shutil.copy(path + x + '/vox' + str(i) + '.wav', final_path + x + '/vocals.wav')                   
            print ('Copy of ' + x + 'directory : in progress 60%\r', end='\r')                   
            shutil.copy(path + x + '/accompaniment' + str(i) + '.wav', final_path + x + '/accompaniment.wav')  
            print ('Copy of ' + x + 'directory : in progress 75%\r', end='\r')                   
            shutil.copy(path + x + '/mixture' + str(i) + '.wav', final_path + x + '/mixture.wav')              
            print ('Copy of ' + x + 'directory : in progress 90%\r', end='\r')                   
            shutil.copy(path + x + '/linear_mixture' + str(i) + '.wav', final_path + x + '/linear_mixture.wav')
            print ('Copy of ' + x + 'directory : in progress 95%\r', end='\r')                   
            shutil.copy(path + x + '/other' + str(i) + '.wav', final_path + x + '/other.wav')                  
            print ('Copy of ' + x + 'directory : in progress 100%')                              
            print (x + ' directory : done')                                                      

        i += 1

