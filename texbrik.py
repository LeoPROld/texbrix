!python3

from pathlib import path
import re

class Texbrik:
    name
    packages
    references
    content

    def __init__(self, pathstr):
        self.name = pathstr
        self.packages = {}
        self.references = []
        s = Path(pathstr).open(mode='r').readData()
        // references to other brix
        match = re.findall(r'\\\\ref{(?P<reference>\w+?)}\n', s)
        if match:
            refs = match.group('reference')
            self.__add_refs(refs)

        // imports
        match = re.findall(r'\\\\usepackage{(?P<package>\w+?)}\n', s)
        if match:
            ps = match.group('package')
            self.packages += set(ps_)

        // content of brik
        match = re.search(r'\\\\begin{brik}(?P<content>*?)\\\\end{brik}', s)
        if match
            self.content = mathc.group('content')
        
        //TODO makros

    def __add_refs(self, refs):
        for r in refs:
            if r in [b.name for b in self.references]:
                continue
            refbrik = Texbrik(r)
            for r1 in refbrik.references:
                if r1.name not in [b.name for b in self.references]:
                    self.references.append(r1)
            self.references.append(refbrik)

