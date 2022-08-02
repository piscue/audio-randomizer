import os
import sys
import wave
import random
import argparse

from alive_progress import alive_bar
from typing import Dict, List


counter = 0


def powoftwo(n: int) -> bool:
    global counter
    counter += 1
    if n % 2 != 0:
        return False
    else:
        if n == 2:
            return True
        return powoftwo(n/2)


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
    if not powoftwo(int(args.splits)):
        print('splits number should be in the power of two'
              + args.splits + ' is not power of two')
        sys.exit(42)
    return parser.parse_known_args()


def split_frames(wavefile: wave.Wave_read, splits: int, duration: int) -> Dict:
    framesdict = {}
    split_duration = duration / splits
    frame_rate = wavefile.getframerate()
    split_readframes_size = split_duration * frame_rate
    actual_position = 1
    with alive_bar(splits, title='Read Frames', force_tty=True) as bar:
        for i in range(splits):
            frame_position = actual_position * frame_rate
            try:
                wavefile.setpos(int(frame_position))
            except wave.Error:
                print(f'Cannot set position to {frame_position} in iteration {i}')
                return framesdict
            framesdict[i] = wavefile.readframes(int(split_readframes_size))
            actual_position += split_duration
            bar()
        return framesdict


def load_wave(fileinput: str, splits: int) -> Dict:
    wavedict = {}
    wavedict['filename'] = fileinput
    wavefile = wave.open(fileinput, mode='rb')
    wavedict['frame_rate'] = wavefile.getframerate()
    wavedict['frames_number'] = wavefile.getnframes()
    wavedict['params'] = wavefile.getparams()
    wavedict['duration'] = wavedict['frames_number'] / wavedict['frame_rate']
    wavedict['frames'] = split_frames(wavefile, splits, wavedict['duration'])
    return wavedict


def list_2_bytes(wavelist: List) -> bytes:
    return b"".join(wavelist)


def randomize_wave(framesdict: Dict, splits: int) -> bytes:
    wavelist = []
    with alive_bar(splits, title='Randomize Wave', force_tty=True) as bar:
        for i in range(splits):
            try:
                key = random.choice(list(framesdict.keys()))
                wavelist.append(framesdict[key])
                del framesdict[key]
            except IndexError:
                print(f'Index out of range, in iteration {i}, returning wave')
                return list_2_bytes(wavelist)
            bar()
    return list_2_bytes(wavelist)


def output_filename(filename: str, splits: str) -> str:
    filenmame_without_extenion = os.path.splitext(filename)[0]
    return filenmame_without_extenion + '_rnd_' + splits + '.wav'


def export_wave(waveresult: bytes, filename: str, params: set, splits: int):
    exportfilename = output_filename(filename, splits)
    exportwave = wave.open(exportfilename, mode='w')
    exportwave.setnchannels(params.nchannels)
    exportwave.setsampwidth(params.sampwidth)
    exportwave.setframerate(params.framerate)
    exportwave.writeframes(waveresult)
    exportwave.close()


if __name__ == "__main__":
    vars, unknown = variables_setup()
    wavedict = load_wave(vars.input, int(vars.splits))
    waveresult = randomize_wave(wavedict['frames'], int(vars.splits))
    export_wave(waveresult, vars.input, wavedict['params'], vars.splits)
