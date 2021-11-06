# Note Recognition model integrated in Bard's Way #
>
> Detailed description of the Note recognition model integrated in Bard's Way
>

## Summary: ##
- Historic
- Integrated model
- Model in training

## Historic: ##

Nothing for now, to be developed in the future.

## Integrated model: ##

Model not integrated for now.

## Model in training: ##

#### General Description: ####

To recognize notes in an instrument we gonna use a multi layer convutionnal neural network.  
To come up with this solution we study many way to recognize note and this one is one of the best. The goal of this network is to convert the wav instrument stem into a midi file. And so with that, the note are recognized.  
The midi file is handwritten so if you write a midi file you already know the note of the song you want to write.  
This type of neural network is designed to recognized image and is used by google image to make the reverse search option.

To have more information about our solution we highly recommend to read our [research paper](./documentation_réseauxNeuronnauxRecoNotes.pdf) (in french)

This neural network output multiple probability matrix. Each matrix is composed of 88 value, each value correspond to one note of the piano and each matrix correspond to one point in time (one matrix every 32ms of music).  
Then we convert this matrix of probability into matrix of note and into a midi file, explain in the [post processing documentation](./documentation_PostProcessingNoteRecognition.md).

#### Instruments note recognized ####

For now we only recognize piano note, because it is, with drums, one of the easiest instrument to work with, it's also one of the most used instrument in song.  
Secondly our model is optimize for piano note, and for other instrument we might risk to change the model.

#### Dataset used: ####

The dataset use is a little odd, it consist of two distinct dataset.  
The acoustic dataset and the language dataset.  

The acoustic dataset is form of approximately 200 piano only song in wav. This dataset is processed for the deep learning to understand the data and is send to the first layer of the network.  
With this dataset the network can train how to recognize piano generally.

The language dataset is form of approximately 200 piano only song in midi (this file are the exact same song as the wav file). This dataset is processed into 32ms portion and each portion is transform into a matrix of 88 value.  
This dataset is then send into the last layer of the network. With this dataset the network can train how to recreate a matrix of 88 value for each 32ms portion of a piano song.

#### Integration: ####

The model is still in training so it's not integrated for now.
