# WAV Merger module for Bard's Way #
>
> Merge instruments tracks in one result WAV file.
>

## Summary: ##
- Usage
- Functions
- Pydub/AudioSegment Data
- Libraries Tested
- Library Used

## Usage: ##
Class `wav_merger` method to merge every tracks of a music.

```python
wav_merger(audio_tracks = list(str()), audio_shifts = list(int()), audio_length = int(), audio_name = str())
```
##  Functions: ##

```python
wav_merger(audio_tracks = list(str()), audio_shifts = list(int()), audio_length = int(), audio_name = str())
```
>
> Merge each audio_tracks in audio\_name respecting them audio\_shifts.
>

#### Parameters: ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**audio_tracks** Array of every instruments path that compose the music.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**audio_shifts** Shift if every instruments in milliseconds.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**audio_length** Length of the music in milliseconds.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**audio_name** Name of the final audio.

##  Pydub/AudioSegment Data: ##

`AudioSegment Object` : Immutable Object representing segment of audio. Filled with these metadata : sample_width, frame_rate, channels and frame_width

`AudioSegment.silent(duration, frame_rate)` returns : AudioSegment object filled with pure digital silence.

`AudioSegment.from_file(path)` return : AudioSegment object based on the file extension.

##  Libraries Tested: ##

- At first we tested a solution with `Numpy` and `Wave` but this solution was too constraining and needed two library to work instead of just one with Pydub. However the Wave library was pretty interesting in its possibility so we are maybe going to use it in our project at some point.

- Then we tested `Audiolab` with `Numpy` again, Audiolab is just a soundfile reader so it's not very usefull for the rest of the project. However this solution was pretty simple and small.

- Next we tested a solution with `The Echo Nest remix API` but this just didn't worked, the fact is that this library use many dependecies with other libraries, so using echonest is too risky, the over thing is their license wich does not allow us to commercialise a project with it.

- And we tested a solution with `librosa`, librosa is very efficient but it's not permetting to do much things with audiofiles, at least not as much as the solution we choose.

##  Library Used: ##

We use `Pydub` and more particulary the `AudioSegment` part of Pydub because it's the simpliest and efficient library to merge two or more wav files. And there is many way to reuse this library for many other purpose link with our project.
`Pydub` got the MIT license. The MIT license is permitting us to commercialise our project with the library it protect, so it's perfect for an EIP project.
