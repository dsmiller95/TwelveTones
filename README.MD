# Setup

Install fluidsynth for audio playback. https://github.com/FluidSynth/fluidsynth/wiki/Download.
Validated to work with fluidsynth-2.4.6-win10-x64 .

Download a soundfont file. some are available [here](https://archive.org/download/free-soundfonts-sf2-2019-04)
place it in SoundFonts and name it `default.sf2`. I used `Creative (emu10k1)8MBGMSFX.SF2`

Set up virtual environment (recommended) and install required packages:

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Running

```shell
python __main__.py
```
