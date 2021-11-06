# Main for Mixing #

## Summary: ##
-mixing2.0.py
-dataset_generator.py
-data-sort.py
-stemmp4creator.py
-trainmodelgenerator.py
-dataset_rename_files.py
-auto_mixing.py
-convert.py


## mixing2.0: ##
Mix the [argument] specified at the execution together following the schema of Musdb18 dataset used by Spleeter

python mixing2.0 [Path/of/music/folder][pattern to mix together][number of mix per music]

#### Parameters: ####


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Path of music folder** : Path to the folder where the music stems are
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Pattern to mix** : Define all pattern to mix together (ex : Drum Bass Gtr Vox)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Number of mix per music** : Choise the number of cut that will be made on the stems for creating a larger dataset



## dataset_generator: ##
Will copy all the mixed files into proper file

python dataset_generator.py [Main Directory][Path to copy][nbr of copy (optional*)]

#### Parameters: ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Main Directory** Path to directory that contain the folders with mixed files.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Path to copy** The path where the dataset will be created.
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Number of copy** this parameter is optional, that will create multiple mix of the same music but at different time of the music

## data-sort: ##
Copy the musics folder in the subfolder of a proper dataset : 01_Drum_Bass_Gtr_Vox, 02_Drum_Bass_Sax etc

python data-sort.py [path to main directory]

#### Parameters: ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Path to main directory** Path to directory that contain all the musics  


## stemmp4creator: ##
Create the .stems.mp4 file correspondent to each music directory (needed for the dataset structur)

python stemmp4creator.py [image path][input.wav][output.stem.mp4]

#### Parameters: ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**image path** : path to the image for the mp4
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**input.wav** : commonly the mixturewav of the music 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**output.stem.mp4** : the name of the output (commonly the name of the directory of the music)


## trainmodelgenerator: ##
Create the .csv config file for spleeter

python trainmodelgenerator.py trainmodelgenerator.py [path to dataset][path to compare dataset][output_train.csv][output_validation.csv]

#### Parameters: ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**path to dataset** : path of the directory that contain the dataset
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**path to compare dataset** : path of the not cut dataset
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**output_train.csv** name of the train csv
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**output_validation.csv** name of the validation csv


## dataset rename file: ##
Rename the files of music's files to match the mixing parameters

python dataset_rename_file.py [path/to/main/folder]

#### Parameters: ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**path to main folder** : path of the directory that contain all the music's directory


## convert ##
Convert all the .wav file with the needed form : 16bit 44000 Khz etc

python convert.py [path/to/main/directory][pcm (PCM_16/PCM_24/PCM_32)]

#### Parameters: ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**path to main directory** : path to the directory that contain the mixed dataset
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**path to main directory** : choose the pcm of the convertion


## auto mixing: ##
Execute mixture2.0.py on each directory in the path given
Execute stemmp4creator on each directory in the path given

python auto_mixing.py [path/to/main/directory]
Need mixture2.0.py in the same folder

#### Parameters: ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**path to main directory** : path where all the music's directory to mix are present


##Order to use##

data-sort > dataset_rename_file  > auto_mixing > dataset_generator > convert > trainmodelgenerator