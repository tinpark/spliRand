# splitRand.py is a python3 script that leverages the power of pydub and librosa to chop up a sound file based on silences detected within it and reorders the slices into new, random structures, as many times as you like. Nice for drum patterns, good for creating new sound structures for game audio libraries, great for making gobbledygook out of spoken word.

# all segments generated have a short fade in and fade out applied to guarantee there are no sample-crossing clicks.

# to install, first get python3 installed on your machine
# make sure pip3 is also installed
# Then install the key python libraries that make this project work:

# pip3 install pydub
# pip3 install librosa
# pip3 install tqdm

# once installed, note the path to this script and note the path to the soundfile you want to chop up and run the script like this:

# python3 path/to/splitRand.py --file=path/to/waveFile.wav
# add arguments to refine the splitting process and define the number of randoms

# python3 path/to/splitRand.py --file=path/to/waveFile.wav --thresh=-60 --msl=10 --fdIn=5 --fdOut=10 --iters= 16

# the above will split your audio at -60dB, whenever it's -60dB to 10ms or more, a fadein of 5ms and fade out of 10ms will be applied to all slices and 16 random iterations of the list of files will be concatenated together to make 16 new .wav files.

# Parts of this script were hacked from the following pages, many thanks.
# https://dataunbox.com/split-audio-files-using-python/
# and
# https://www.thepythoncode.com/article/concatenate-audio-files-in-python


# import all the core python things you need
import os, random, glob, argparse, time
# load in tqdm
from tqdm import tqdm
# load in pydub system
from pydub import AudioSegment
from pydub.silence import split_on_silence

# deal with arguments from the commandline
parser = argparse.ArgumentParser()
parser.add_argument('--msl', type=int, help='minimum silence length in ms', default=5)
parser.add_argument('--thresh', type=float ,help='onset threshold in dB', default=-60)
parser.add_argument('--fdIn', type=int, help='fadein time in ms', default=4)
parser.add_argument('--fdOut', type=int, help='fadeout time in ms', default=4)
parser.add_argument('--iters', type=int, help='set the number of random sound files you want to generate', default=6)
parser.add_argument('--file', type=str, help='specify the file you want to work on')
args = parser.parse_args()

# define the arguments as functions you can call later in the script
fadeInTime=args.fdIn
fadeOutTime=args.fdOut
minSilence=args.msl
threshold=args.thresh
iterations=args.iters
soundFile=args.file

# print what you set as your arguments, or print the defaults
print(fadeInTime, fadeOutTime, minSilence, threshold, iterations)

# get the path where you're working in the terminal
path = os.path.dirname(soundFile)
absPath = os.path.abspath(path)
print(absPath)
# get a list of files in that path
#files = os.listdir(path)

# find .wav files in your folder and for each soundfile, run this sequence:


# make a folder for your audio slices from each master wave file that is found in your folder
soundPath = os.path.basename(soundFile).split('.')[0]
if not os.path.exists(soundPath):
    os.makedirs(soundPath)
chunkPath = os.path.join(absPath, soundPath)

#create a path for your random structures inside your slices directory
randomsPath = os.path.join(chunkPath, "randoms")
if not os.path.exists(randomsPath):
    os.makedirs(randomsPath)

# segment audio
sound_file = AudioSegment.from_wav(soundFile)
audio_chunks = split_on_silence(sound_file, min_silence_len=minSilence, silence_thresh=threshold)

# export segemented audio with short fade in and out
for i, chunk in enumerate(audio_chunks):
    out_file = os.path.join(chunkPath, f'{soundPath}_{i}.wav'.format(i))
    print("exporting", out_file)
        # add short 4ms fade in and fade out
    awesome = chunk.fade_in(fadeInTime).fade_out(fadeOutTime)
    # write files to disk
    awesome.export(out_file, format="wav")

# you have now made a large pile of sound files, next make some random ordering of the files and concatenate them together, writing a new file each time.

# get the number of new Random Files you want and set this part of the script to run that number of times.

pathOfChunks=os.path.join(absPath, chunkPath)
print(pathOfChunks)

os.chdir(pathOfChunks)
# get a list of .wav files together from the chunks directory
files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".wav")]

#print(files)
# get length of the list
length = len(files)
#print(length)

os.chdir(absPath)

num = iterations
for i in range(num):
    # create the randomFileName
    randomFileName = os.path.join(randomsPath, f'{soundPath}_rnd_{i}.wav')
    randomTextFileName = os.path.join(randomsPath, f'{soundPath}_rnd_{i}.txt')
    randomMp3Name = os.path.join(randomsPath, f'{soundPath}_rnd_{i}.mp3')

    # randomize the sound file list
    # next up chance to weight randomness and make more musical structures

    rando = random.sample(files, length)

    # uncomment this if you want to write a text file of the random ordering, for reference
    #with open(randomTextFileName, "w") as output:
    #    output.write(str(rando))

    # prepare files for export
    clips = []
    for f in rando:
        clip = AudioSegment.from_wav((os.path.join(chunkPath, f)), "wav")
        clips.append(clip)

    final_clip = clips[0]
    range_loop = tqdm(list(range(1, len(clips))), "Concatenating audio")
    for i in range_loop:
        final_clip = final_clip + clips[i]
        # export the final clip
        final_clip.export(randomFileName, format="wav")
        # uncomment if you want mp3s as well
        #   final_clip.export(randomMp3Name, format="mp3")
