# Temporal Frequency Analyser module for Bard's Way #
>
> Split WAV file in sample of 32ms and 960ms.
>

## Summary: ##
- Usage
- Functions
- Pydub.AudioSegment & Numpy
- Library Used

## Usage: ##
Class `tempo_frequency_analyser` method to merge every tracks of a music.

```python
tempo_frequency_analyser(audio = pydub.AudioSegment)
```
##  Functions: ##

```python
tempo_frequency_analyser(audio = pydub.AudioSegment)
```
>
> An array of array of AudioSegment construct as a[b[object]] where:
>    a where len(a) duration / 960ms.
>    b where b[x] <= 30 because 30 * 32ms = 960ms.
>    object as an AudioSegment of 32ms.
>

#### Parameters: ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**audio** AudioSegment object of the WAV file.

### Return: ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;array[array[AudioSegment]].

##  Pydub.AudioSegment & Numpy: ##

`AudioSegment Object` : Immutable Object representing segment of audio. Filled with these metadata : sample_width, frame_rate, channels and frame_width

`AudioSegment.duration_seconds(path)` return : AudioSegment object duration in ms.

`Numpy.arange` : range from X to Y with step of I.

##  Library Used: ##

We use `Pydub` and more particulary the `AudioSegment` part of Pydub because it's the simpliest and efficient library to merge two or more wav files. And there is many way to reuse this library for many other purpose link with our project.
`Pydub` got the MIT license. The MIT license is permitting us to commercialise our project with the library it protect, so it's perfect for an EIP project.
