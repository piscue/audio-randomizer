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
    dict_wave = {}
    dict_wave['filename'] = fileinput
    wavefile = wave.open(fileinput, mode='rb')
    dict_wave['audio_frames'] = wavefile.getnframes()
    dict_wave['params'] = wavefile.getparams()
    dict_wave['wave'] = wavefile.readframes(dict_wave["audio_frames"])
    return dict_wave


if __name__ == "__main__":
    vars, unknown = variables_setup()
    wavedict = load_wave(vars.input)
