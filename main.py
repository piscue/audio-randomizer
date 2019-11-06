import wave
import argparse
import sys
from typing import Dict


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


def load_wave(fileinput: str) -> Dict:
    wavedict = {}
    wavedict['filename'] = fileinput
    wavefile = wave.open(fileinput, mode='rb')
    wavedict['audio_frames'] = wavefile.getnframes()
    wavedict['params'] = wavefile.getparams()
    wavedict['wave'] = wavefile.readframes(wavedict["audio_frames"])
    return wavedict



if __name__ == "__main__":
    vars, unknown = variables_setup()
    wavedict = load_wave(vars.input)
