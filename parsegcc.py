#!/usr/bin/env python3

import sys
from pathlib import Path
import code
import sys
import argparse
import pickle

from lib.parse import parseGcc, parseLinker

tmp_path = Path(__file__).parent / "tmp"
if not tmp_path.exists():
    tmp_path.mkdir()

pickle_path = tmp_path /  "parsed.pickle"


def parse_from_stdin():
    contents = sys.stdin.read()

    compiler = parseGcc(contents)
    linker = parseLinker(contents)

    both = (compiler, linker)

    with open(pickle_path, "wb") as pickle_file:
        pickle.dump(both, pickle_file)

    print("Done!")

def run_interactive(compiler, linker):
    code.interact(local=locals())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", action="store_true")

    args = parser.parse_args()

    if args.i:
        with open(pickle_path, "rb") as pickle_file:
            both = pickle.load(pickle_file)

        (compiler, linker) = both
        run_interactive(compiler, linker)
    else:
        parse_from_stdin()
