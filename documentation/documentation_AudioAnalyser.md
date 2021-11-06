# Audio Analyser class for Bard's Way #
>
> Aggregate the audio analysis modules in one place
>

## Summary ##
  - [Usage](#usage)
  - [Analysis Structure](#analysis-structure)
      - [Example](#example)
  - [Constructor](#constructor)
      - [Parameters](#parameters)
  - [Attributes](#attributes)
  - [Methods](#methods)
      - [Parameters](#parameters-1)
      - [Return Value](#return-value)


## Usage ##
Instantiate an `AudioAnalyser` object. You can specify the sampling frequency via the `frequency_sampling` optional constructor parameter and property.

Use the method `AudioAnalyser.analyse` to perform a batch of audio analysis on a given audio file.



```python
AudioAnalyser(frequency_sampling = int(32e3))

AudioAnalyser.sampling_requency = int()

AudioAnalyser.analyse(raw_audio = pydub.AudioSegment(), path = str())
```

## Analysis Structure ##
The analysis returns an array with one element per audio channel (useful for a stereo or multi-track file) containing a list of dictionaries with the following items:
*  `stft`: Short Time Fourier Transform
*  `dwt`: Discrete Wavelet Transform
*  `ae`: Amplitude Envelope
*  `as`: Attack Segment
*  `ss`: Silence Segment

##  Constructor ##

```python
AudioAnalyser(frequency_sampling = int(32e3))
```
>
> Insantiate an AudioAnalyser object.
>

#### Parameters ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**frequency_sampling**: Sampling frequency of the analysis (*default: 32kHz*)

##  Attributes ##

```python
frequency_sampling = int()
```
>
> The sampling frequency of the analysis
>

## Methods ##
```python
analyze(raw_audio: pydub.AudioSegment(), path: str())
```
>
> Run the analysis on a specified audio file
>
#### Parameters ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**raw_audio**: Audio file to run the analysis on.
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**path**: Path to the analysis folder
#### Return Value ####
An analysis object. See [Analysis Structure](#analysis-structure) for more information.
