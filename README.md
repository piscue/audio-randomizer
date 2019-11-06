# Audio Randomizer

## Description

This is a tool to randomize a audio file itself. It can be used on any Wave file. The tool will split it into chunks of the same size, sort it randomly and merge it on a new created wave file.

As a constrain, to don't do glitches, I've set the number of chunks it has to be a power of 2 (2, 4, 8, 16, 32, 64, 128, and so on). In my results with this number it behaves well.

It will maintain the same settings and duration of the original audio file.

## Usage

You can specify the Wave file to use and the number of chunks


```
# -i / --input: Specify the source wave file
# -s / --split: Number of chunks to split

python3 main.py -i original.wav -s 128
```
