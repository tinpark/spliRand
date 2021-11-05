# splitRand
Simple python script to split audio at silences and reconcatenate into a series of new, randomly structured files

# Introduction
`splitRand.py` is a `python3` script that leverages the power of `pydub` and `librosa` to chop up a sound file based on silences detected within it. It then reorders the slices into new, random structures, as many times as you like. Nice for drum patterns, good for creating new sound structures for game audio libraries, great for making gobbledygook out of spoken word.

All segments generated have a short fade in and fade out applied to guarantee there are no sample-crossing clicks.

# Installation and dependencies

To install, first get python3 installed on your machine.

## Windows python3 instructions

- download: <https://www.python.org/downloads/windows/>
- installation reading: <https://docs.python.org/3/using/windows.html>

## OSX python3 installation

- install brew [instructions here](https://brew.sh/)
- then install python `brew install python`
- further reading: <https://docs.python-guide.org/starting/install3/osx/>

## install dependencies with pip3

### pydub
`pydub` is an awesome toolkit developed by [James Robert](https://github.com/jiaaro) and explained here: <http://pydub.com/>

`pip3 install pydub`

### librosa
I'm not sure if `Librosa` is really needed for this script, but as you might ultimately want to produce graphs of audio data or to make more sophsiticated splitting of audio, this might be a useful tool to have access to. `Librsoa` is explained here <https://librosa.org/doc/latest/index.html>.

`pip3 install librosa`

### tqdm

This is not important but it helps you to see how much longer you've got before the process is completed. Can be reassuring for very long processes.

More information is available here: <https://github.com/tqdm/tqdm>

`pip3 install tqdm`
  
### ffmpeg

Insanely useful media file manager, you'll need it anyway

`brew install ffmpeg`

## think about where you'd like to keep this script and make a note of the path

once installed, note the path to this script so that you can call it on the commandline:

`python3 path/to/splitRand.py --file=path/to/waveFile.wav`

# Download the package

Either download the zip of this repository or clone it:

`git clone https://github.com/tinpark/spliRand.git`

# Arguments
Add arguments to refine the splitting process and define the number of new random files:

`python3 path/to/splitRand.py --file=path/to/waveFile.wav --thresh=-60 --msl=10 --fdIn=5 --fdOut=10 --iters=16`

The above will split your audio at whenever it's dropped to **-60dB** for **10ms** or more, a fadein of *5ms* and fade out of *10ms* will be applied to all slices and 16 random iterations of the short segments files will be concatenated together to make 16 new `.wav` files.

# example python calls

Try the following examples to test things.

First `cd` into the folder you downloaded or cloned from github.

Then run this line of code

`python3 splitRand.py --file="examples/Herve_klezmer1.wav" --thresh=-60 --msl=5 --iters=4`

`python3 splitRand.py --iters=6 --file="examples/Drum160Fight.wav" --thresh=-10 --msl=5`

`python3 splitRand.py --iters-12 --file="examples/martin.wav" --thresh=-30 --msl=5`

# Credits:
Parts of this script were hacked from the following pages, many thanks especially to:
- <https://dataunbox.com/split-audio-files-using-python/>
- <https://www.thepythoncode.com/article/concatenate-audio-files-in-python>
