#!python3

from pathlib import Path
import re

NAMEPAT = re.compile(r'\\brik{(?P<name>[\w\W]+?)}')
PREREQS = re.compile(r'\\prerequisite{(\w+?)}')
INCLS = re.compile(r'\\include{(\w+?)}')
BRIKCONTENT = re.compile(r'\\begin{content}(?P<content>[\w\W]*?)\\end{content}')
 
class Texbrik:
    def __init__(self, name, prerequisites, includes, content):
        self.name = name
        self.prerequisites = prerequisites
        self.includes = includes
        self.content = content


def brikFromDoc(pathstr):
    s = Path(pathstr).read_text()

    n = NAMEPAT.findall(s)
    if len(n) is not 1:
        raise InputError(pathstr, 'none or too many names')
    
    c = BRIKCONTENT.findall(s)
    if len(c) is not 1:
        raise InputError(pathstr, 'none or too many content blocks')

    return Texbrik(
        name            = n[0],
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
