#!python3

from pathlib import Path
from string import Template
import re

PREREQS = re.compile(r'\\prerequisite{(?P<relativepath>[/_\w]+?)}')
BRIKINSERTS = re.compile(r'\\brikinsert{(?P<relativepath>[/_\w]+?)}')
PKGS = re.compile(r'\\usepackage{(\w+?)}')
BRIKCONTENT = re.compile(r'\\begin{content}([\w\W]*?)\\end{content}')
 
class Texbrik:
    def __init__(self, root_dir, relative_path, prerequisites, packages, content):
        self.root_dir       = root_dir
        self.relative_path  = relative_path
        self.packages       = set(packages)
        self.content        = content
        self.prerequisites  = prerequisites
        self.brikinserts    = dict()
        self.expanded       = False
        self.ignore         = set()
        
    def __eq__(self, other):
        return self.relative_path == other.relative_path

    def expand(self, ignore=set()):
        self.ignore |= ignore
        if self.expanded:
            return
        self.brikinserts    = dict([
            (b, brikFromDoc(self._relative_pathstring_to_path(b), self.root_dir))
            for b in BRIKINSERTS.findall(self.content)
        ])
        self.content = BRIKINSERTS.sub(self._process_brikinsert_occurrence, self.content)

        s = ""
        for p in self.prerequisites:
            if p in self.ignore:
                continue
            try:
                b = brikFromDoc(self._relative_pathstring_to_path(p), self.root_dir)
            except InputError as e:
                raise InputError(str(self.relative_path), 'Failed to proces prerequisite ' + p) from e
            b.expand(ignore = self.ignore)
            self.ignore |= b.ignore
            self.ignore.add(p)
            self.packages |= b.packages
            s += b.content

        self.content = s \
                + "\n%From TeXBriK [{relative_path}]\n".format(relative_path=str(self.relative_path)) \
                + self.content \
                + "\n%End of TeXBriK [{relative_path}]\n".format(relative_path=str(self.relative_path))
        self.expanded = True

    def _process_brikinsert_occurrence(self, match_object):
        p = match_object[1]
        b = self.brikinserts[match_object[1]]
        b.expand(ignore=self.ignore)
        self.packages |= b.packages
        self.ignore |= b.ignore
        self.ignore.add(p)
        return b.content

    def _relative_pathstring_to_path(self, relative_pathstring):
        return self.root_dir.joinpath(relative_pathstring).with_suffix('.brik')

    def expanded_content(self):
        self.expand()
        return self.content

    def make_TeX_file(self, template = Path(__file__).resolve().parent.joinpath('default_template')):
        self.expand()
        t = Template(template.read_text())
        packages = '\n'.join(['\\usepackage{{{}}}'.format(i) for i in self.packages])
        return t.substitute(
            packages    = packages,
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
        packages        = PKGS.findall(s),
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
