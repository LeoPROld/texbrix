#!python3

from pathlib import Path
import re

PREREQS = re.compile(r'\\brikinsert{(?P<relativepath>[/_\w]+?)}')
INCLS = re.compile(r'\\include{(\w+?)}')
BRIKCONTENT = re.compile(r'\\begin{content}([\w\W]*?)\\end{content}')
 
class Texbrik:
    def __init__(self, prerequisites, includes, content, root_dir):
        self.root_dir = root_dir
        self.includes = set(includes)
        self.content = content
        self.prerequisites = dict([
                (p, brikFromDoc(root_dir.joinpath(p).with_suffix('.brik'), self.root_dir))
                for p in prerequisites
            ])
        self.expanded = False

    def expand(self):
        if self.expanded:
            return

        for p in self.prerequisites.values():
            p.expand()
            self.includes = self.includes.union(p.includes)
        self.content = PREREQS.sub((lambda m: self.prerequisites[m[1]].expanded_content()), self.content)

        self.expanded = True

    def expanded_content(self):
        self.expand()
        return self.content

def brikFromDoc(path, root_dir):

    if not root_dir.is_dir():
        raise NotADirectoryError('specified project root_dir is not a directory')
    if not (path.is_file() and path.suffix == '.brik'):
        path = path.relative_to(root_dir)
        raise InputError(str(path), '{brik} is not a TeXBriK'.format(brik=str(path)))
    s = path.read_text()

    c = BRIKCONTENT.findall(s)
    if len(c) != 1:
        raise InputError(pathstr, 'none or too many content blocks')

    return Texbrik(
        prerequisites   = PREREQS.findall(s),
        includes        = INCLS.findall(s),
        content         = c[0],
        root_dir        = root_dir
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
