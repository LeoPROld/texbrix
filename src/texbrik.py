#!python3

from pathlib import Path
from string import Template
import re

PREREQS = re.compile(r'\\prerequisite{(?P<relativepath>[/_\w]+?)}')
BRIKINSERTS = re.compile(r'\\brikinsert{(?P<relativepath>[/_\w]+?)}')
INCLS = re.compile(r'\\include{(\w+?)}')
BRIKCONTENT = re.compile(r'\\begin{content}([\w\W]*?)\\end{content}')
 
class Texbrik:
    def __init__(self, root_dir, relative_path, prerequisites, includes, content):
        self.root_dir       = root_dir
        self.relative_path  = relative_path
        self.includes       = set(includes)
        self.content        = content
        self.prerequisites  = prerequisites
        self.brikinserts    = dict()
        self.expanded       = False
        self.processed_brix = set()
        
    def __eq__(self, other):
        return self.relative_path == other.relative_path

    def expand(self, ignore={}):
        if self.expanded:
            return
        self.brikinserts    = dict([
            (b, brikFromDoc(self._relative_pathstring_to_path(b), self.root_dir))
            for b in BRIKINSERTS.findall(self.content)
        ])
        self.content = BRIKINSERTS.sub(self._process_brikinsert_occurrence, self.content)

        s = ""
        for p in self.prerequisites:
            if p in self.processed_brix:
                continue
            b = brikFromDoc(self._relative_pathstring_to_path(p), self.root_dir)
            b.expand(ignore = self.processed_brix)
            self.processed_brix |= b.processed_brix
            self.includes |= b.includes
            s += b.content

        self.content = s + self.content
        self.expanded = True

    def _process_brikinsert_occurrence(self, match_object):
        p = self.brikinserts[match_object[1]]
        p.expand()
        self.includes |= p.includes
        self.processed_brix = self.processed_brix.union(p.processed_brix)
        return p.content

    def _relative_pathstring_to_path(self, relative_pathstring):
        return self.root_dir.joinpath(relative_pathstring).with_suffix('.brik')

    def expanded_content(self):
        self.expand()
        return self.content

    def make_TeX_file(self, template = Path(__file__).resolve().parent.joinpath('TeX_template')):
        self.expand()
        t = Template(template.read_text())
        includes = '\n'.join(['\\include{{{}}}'.format(i) for i in self.includes])
        return t.substitute(
            includes    = includes,
            content     = self.content
        )

def brikFromDoc(path, root_dir):

    if not root_dir.is_dir():
        raise NotADirectoryError('specified project root_dir is not a directory')
    if not (path.is_file() and path.suffix == '.brik'):
        path = path.relative_to(root_dir)
        raise InputError(str(path), '{brik} is not a TeXBriK'.format(brik=str(path)))
    s = path.read_text()

    c = BRIKCONTENT.findall(s)
    if len(c) != 1:
        raise InputError(str(path), 'none or too many content blocks')

    return Texbrik(
        root_dir        = root_dir,
        relative_path   = path.relative_to(root_dir),
        prerequisites   = PREREQS.findall(s),
        includes        = INCLS.findall(s),
        content         = c[0]
    )

class InputError(Exception):
    """Exception raised for errors on the input.

    Attributes:
    expression: input expression in which the error occured
    message: explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
