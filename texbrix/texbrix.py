#!python3
from .texbrik.texbrik import brikFromDoc
import argparse
from pathlib import Path

__version__ = "0.2.0"
parser = argparse.ArgumentParser(description='create LaTeX file from brix')
parser.add_argument(
    'top_brik',
    metavar='Top Brik',
    type=str,
    help='top .brik document to work with')
parser.add_argument('-template', nargs=1)


def main():
    args = parser.parse_args()
    p = Path(args.top_brik).resolve()
    b = brikFromDoc(p)
    if args.template:
        s = b.make_TeX_file(template=Path(args.template[0]).resolve())
    else:
        s = b.make_TeX_file()
    p.with_suffix('.tex').write_text(s)
