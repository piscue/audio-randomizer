# Audio Randomizer

## Description

This is a tool to randomize a audio file itself. It can be used on any Wave file. The tool will split it into chunks of the same size, sort it randomly and merge it on a new created wave file.

It will aim to maintain the same settings and duration of the original audio file.

## Usage

You can specify the Wave file to use and the number of chunks


```
# -i / --input: Specify the source wave file
# -s / --split: Number of chunks to split

python3 main.py -i original.wav -s 128
```

or by using Docker:

```
docker run -v ~/Downloads:/wav piscue/audio-randomizer -i /wav/source.wav -s 256
```

## Pipenv

The requirements are created using pipenv. In order to use the same environment you can run:

```pipenv shell```

## Docker usage
If you want to run via container you can also build the image yourself:

```
docker build -t piscue/audio-randomizer .
docker run -v ~/Downloads:/wav piscue/audio-randomizer -i /wav/source.wav -s 2
```

or run directly from Docker hub:

```
docker run -v ~/Downloads:/wav piscue/audio-randomizer -i /wav/source.wav -s 2
```

The argument ```-v``` binds in that case the Downloads folder on your host into a /wav folder in the container
