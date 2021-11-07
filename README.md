<img src="logo.svg" alt="bardsway" width="128" height="128"/><br/>

# Bard's way #
![pytest](https://github.com/deezer/spleeter/workflows/pytest/badge.svg)![coverage](https://img.shields.io/badge/coverage-97%25-green)![python](https://img.shields.io/badge/python-3.8-yellow)![spleeter](https://img.shields.io/badge/spleeter-2.0-blue)![size](https://img.shields.io/badge/size-too%20much-red)![tensorflow](https://camo.githubusercontent.com/7ce7d8e78ad8ddab3bea83bb9b98128528bae110/68747470733a2f2f616c65656e34322e6769746875622e696f2f6261646765732f7372632f74656e736f72666c6f772e737667)

### EIP 2021 by alzate_j brihou_b ghiren_a hazard_v devier_n karaog_c cauqui_a ###

>
> Bard's way is an algorithm that separates the instruments of an audio file sent in input
> and return in output the partitions of said instruments into JSON files.
>

## Quick start ##
You can download it from our [GitHub Releases](https://github.com/brihoumb/bardsway/releases).  

Or use **Bard's Way** with your local python installation by using the requirement.txt in scripts and running:
```sh
python software/__main__.py
```

## Documentation and index ##

- [x] Docker container
- [x] [Environement](documentation/documentation_Env.md)
- [x] [Environement on windows](documentation/documentation_Windows.md)
- [x] [Organisational documentation](documentation/documentation_Organisationnelle.docx)
- [x] [Showcase website](https://eip.epitech.eu/2021/bardsway/)
- [x] [Installer](documentation/documentation_BardswayInstaller.md)
- [x] [How to compile](documentation/documentation_HowToCompile.md)
- [x] [Server](documentation/documentation_server.md)
- [x] [Database](documentation/documentation_Database.md)
- [Front]
  - [x] [Stripe Payment](documentation/documentation_stripePayment.md)
  - [x] Website
  - [x] Software
- Software:
  - [x] [BardsWay](documentation/documentation_BardsWay.md) (Main of the project)
  - [x] [Graphical Display](documentation/documentation_GraphicalDisplay.md)
  - **DEPRECATED** Module Analyser:
	- [x] [Amplitude Enveloppe](documentation/documentation_AmplitudeEnvelope.md)
	- [x] [AudioAnalyser](documentation/documentation_AudioAnalyser.md)
    - [x] [Data Formating](documentation/documentation_DataFormating.md)
    - [x] [Discrete Wavelet Transform](documentation/documentation_DiscreteWaveletTransform.md)
    - [x] [Fast Fourier Transform](documentation/documentation_FastFourierTransform.md)
    - [x] [Four Second Splitter](documentation/documentation_FourSecondSpliter.md)
    - [x] [FrequencySampling](documentation/documentation_FrequencySampling.md)
    - [x] [JSON writer](documentation/documentation_JSONwriter.md)
    - [x] [Mixing](documentation/documentation_Mixing.md)
    - [x] [Normaliser](documentation/documentation_Normaliser.md)
    - [x] [Output](documentation/documentation_OutputWriter.md)
    - [x] [Sample Randomiser](documentation/documentation_SampleRandomiser.md)
    - [x] [Short Time_Fourier Transform](documentation/documentation_ShortTimeFourierTransform.md)
    - [x] [Silent and Attack Segment](documentation/documentation_SilenceAndAttackSegment.md)
    - [x] [Temporal Frequency Analyser](documentation/documentation_TemporalFrequencyAnalyser.md)
    - [x] [Wav Merger](documentation/documentation_WAVmerger.md)
  - Deep Learning :
    - [x] [Note Recognition Model](documentation/documentation_NoteRecognitionModel.md)
    - [x] [Post Processing Note Recognition](documentation/documentation_PostProcessingNoteRecognition.md)
    - [x] [Spleeter Model](documentation/documentation_SpleeterModel.md)
    - [x] [Spleeter 2.0](documentation/documentation_Spleeter2.md)
- Research :
  - [x] [Neural Network](documentation/documentation_réseauxNeuronnauxRecoNotes.pdf)

## Licensing ##

The code of **Spleeter** is [MIT-licensed](https://github.com/deezer/spleeter/blob/master/LICENSE).
```BibTeX
@article{spleeter2020,
  doi = {10.21105/joss.02154},
  url = {https://doi.org/10.21105/joss.02154},
  year = {2020},
  publisher = {The Open Journal},
  volume = {5},
  number = {50},
  pages = {2154},
  author = {Romain Hennequin and Anis Khlif and Felix Voituret and Manuel Moussallam},
  title = {Spleeter: a fast and efficient music source separation tool with pre-trained models},
  journal = {Journal of Open Source Software},
  note = {Deezer Research}
}
```
