# Frequency Sampling module for Bard's Way #
>
> Convert the audio to 32kHz.
>

## Summary: ##
- Usage
- Functions
- Pydub.AudioSegment Data
- Library Used

## Usage: ##
Function `frequency_sampling` method open a WAV from path and change it to 32kHz.

```python
frequency_sampling(path = str())
```
##  Functions: ##

```python
frequency_sampling(path = str())
```
>
> Return an AudioSegment of the WAV path given as parameter and change it's frequency to 32kHz'.
>

#### Parameters: ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**path** The path to the WAV file.

### Return: ###
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Pydub.AudioSegment().

##  Pydub.AudioSegment Data: ##

`AudioSegment Object` : Immutable Object representing segment of audio. Filled with these metadata : sample_width, frame_rate, channels and frame_width

`AudioSegment.set_frame_rate(frame_rate)` returns : Creates an equivalent version of this AudioSegment with the specified frame rate (in Hz).

`AudioSegment.from_wav(path)` return : AudioSegment object based on the WAV extension.

##  Library Used: ##

We use `Pydub` and more particulary the `AudioSegment` part of Pydub because it's the simpliest and efficient library to merge two or more wav files. And there is many way to reuse this library for many other purpose link with our project.
`Pydub` got the MIT license. The MIT license is permitting us to commercialise our project with the library it protect, so it's perfect for an EIP project.
