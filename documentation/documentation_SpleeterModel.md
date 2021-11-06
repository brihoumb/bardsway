# Spleeter Model integrated in Bard's Way #
>
> Detailed description of the Spleeter model integrated in Bard's Way
>

## Summary: ##
- Historic
- Integrated model
- Model in training

## Historic: ##

Nothing for now, to be developed in the future.

## Integrated model: ##

#### General Description: ####

The current integrated model, is the basic model given by Spleeter themselves.  
We implemented the basic model because we needed it to collect beta feedback as soon as possible.  
The training for our Spleeter model is currently too long and need a proper computer specialized in deep learning training to be complete and functional.  
So this is why we decided to implement the basic Spleeter model, but this is a temporary solution, and it will be replace when our model training is over.

#### Instruments separated: ####

For now the basic Spleeter model separate with different stems describe like this :
- 2 stems : Vocal - Instruments
- 4 stems : Vocal - Drums - Bass - Other
- 5 stems : Vocal - Drums - Bass - Piano - Other.

#### Dataset used: ####

To do their training Spleeter team used the musdb Dataset. It's a dataset composed of 150 tracks, each tracks is separated like this :  
Mixture.wav - Vocal.wav - Drums.wav - Bass.wav - Other.wav  

To learn more about musdb dataset go to this website :  
https://sigsep.github.io/datasets/musdb.html#musdb18-compressed-stems

#### Integration: ####

To integrate the model, we encountered many problems, but the bigger one was the installation of Tensorflow and it's dependencies, particularly FFMPEG, which is very complicated to make it work on Windows.  
But now that we managed to make it work, implement the next model will be much easier.

## Model in training: ##

#### General Description: ####

To propose something new with our project, we decided to train the Spleeter deep learning with our dataset to improve it and create a Spleeter model with new instruments recognized.  
With this we can propose a new approach to Spleeter and justify the usage of it and the general work on our project.  
The final goal is to have an improve version of the basic Spleeter model.

#### Instruments separated: ####

For now we decided which instrument will be new, but we did not decided in which stems.  
We gonna add 3 new instruments,
The only thing we are sure is we gonna keep the original stems like this :  
- 2 stems : Vocal - Instruments
- 4 stems : Vocal - Drums - Bass - Other
- 5 stems : Vocal - Drums - Bass - Piano - Other  

And the major idea for now is to add our stems back to the original 5 stems like this :  
 - 8 stems : Vocal - Drums - Bass - Piano - Saxophone - Synth - Guitar - Other

#### Dataset used: ####

For our new model we used a part of musdb dataset and the Cambridge dataset.  
The Cambridge dataset is a free collection of music tracks with their instruments separated. We decided to use the Cambridge dataset because there is tracks with the new instrument we want to implement. We also use the musdb dataset because it is a safe bet to get proper recognition of the original instruments.

To learn more about the Cambridge dataset or to download a song from the Cambridge dataset go to this website:  

https://multitracksearch.cambridge-mt.com/ms-mtk-search.htm  


#### Integration: ####

The model is still in training so it's not integrated for now.
