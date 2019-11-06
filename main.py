import os
import sys
import wave
import random
import argparse

from typing import Dict, List


def variables_setup():
    parser = argparse.ArgumentParser(description='Process Env and Svc')
    parser.add_argument('--input', '-i')
    parser.add_argument('--splits', '-s')
    args = parser.parse_args()
    if not args.input:
        print('missing input wave file')
        sys.exit(42)
    if not args.splits:
        print('missing number of splits')
        sys.exit(42)
    return parser.parse_known_args()


def split_frames(frames: int, splits: int, frames_number: int) -> Dict:
    framesdict = {}
    x = 0
    chunksize = frames_number / splits
    for i in range(splits):
        curFrame = frames[x:(x+int(chunksize))]
        x=x+int(chunksize)
        framesdict[i] = curFrame
        i += 1
    return framesdict


def load_wave(fileinput: str, splits: int) -> Dict:
    wavedict = {}
    wavedict['filename'] = fileinput
    wavefile = wave.open(fileinput, mode='rb')
    wavedict['frame_rate'] = wavefile.getframerate()
    wavedict['frames_number'] = wavefile.getnframes()
    wavedict['params'] = wavefile.getparams()
    wavedict['duration'] = wavedict['frames_number'] / wavedict['frame_rate']
    all_frames = wavefile.readframes(wavedict['frames_number'])
    wavedict['frames'] = split_frames(all_frames, splits,
                                      wavedict['frames_number'])
    return wavedict


def randomize_wave(framesdict: Dict, splits: int) -> List:
    wavelist = []
    for i in range(splits):
        key = random.choice(list(framesdict.keys()))
        wavelist.append(framesdict[key])
        del framesdict[key]
    return wavelist


def output_filename(filename: str) -> str:
    filenmame_without_extenion = os.path.splitext(filename)[0]
    return filenmame_without_extenion + '_rnd.wav'


def export_wave(waveresult: bytes, filename: str, params: set):
    exportfilename = output_filename(filename)
    exportwave = wave.open(exportfilename, mode='w')
    exportwave.setparams(params)
    exportwave.writeframes(waveresult)


if __name__ == "__main__":
    vars, unknown = variables_setup()
    wavedict = load_wave(vars.input, int(vars.splits))
    wavelist = randomize_wave(wavedict['frames'], int(vars.splits))
