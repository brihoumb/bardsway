# ![Bard's Way logo](logo.svg)
![pytest](https://github.com/deezer/spleeter/workflows/pytest/badge.svg)![coverage](https://img.shields.io/badge/coverage-97%25-green)![python](https://img.shields.io/badge/python-3.7.3-yellow)![spleeter](https://img.shields.io/badge/spleeter-1.5.4-blue)![size](https://img.shields.io/badge/size-too%20much-red)![tensorflow](https://camo.githubusercontent.com/7ce7d8e78ad8ddab3bea83bb9b98128528bae110/68747470733a2f2f616c65656e34322e6769746875622e696f2f6261646765732f7372632f74656e736f72666c6f772e737667)

## Author
##### alzate_j brihou_b cauqui_a devier_n ghiren_a hazard_v karaog_c

## Quick start
Either download from our [GitHub Releases](https://github.com/brihoumb/bardsway/releases) or our [Website](https://eip.epitech.eu/2021/bardsway/).  

To use **Bard's Way** you can use our integrated GUI and give a WAV audio file or use it in command line from an example audio file:
```bash
# Separate the example audio into 5 components (bass, drum, piano, voice, other)
bardsway[.exe] audio_example.wav
```

## About

**Bard's way** is a source separation and notes recognition algorithm with pretrained models written in *[Python](https://www.python.org/)* and uses *[Tensorflow](https://tensorflow.org/)* and *[Spleeter](https://github.com/deezer/spleeter)*.

It was developed by 7 master degree students as a project graduation.

## License

The code of **Spleeter** is [MIT-licensed](LICENSE).
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
