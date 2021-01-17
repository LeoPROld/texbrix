#!python3
import argparse
from texbrik import *
from pathlib import Path

parser = argparse.ArgumentParser(description='create LaTeX file from brix')
parser.add_argument('top_brik', metavar='Top Brik', type=str, help='top .brik document to work with')

def main():
    args = parser.parse_args()
    p = Path(args.top_brik).resolve()
    b = brikFromDoc(p, p.parent)
    s = b.make_TeX_file()
    print(s)


if __name__ == '__main__':
    main()