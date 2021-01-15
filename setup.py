from pathlib import Path
from setuptools import setup

def read(fname):
    return Path(__file__).resolve().parent.joinpath(fname).open().read()

setup(
    name = "TeXBriX",
    version = "0.0.1",
    author = "Leopold Fajtak",
    author_email = "leopold@fajtak.at",
    description = "A granular approach to LaTeX",
    license = "GPLv3",
    keywords = "mathematics dependencies layout filestructure"
    url = "http://github.com/leopoldfajtak/texbrix"
    packages = [],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing :: Markup :: LaTeX"
        ]
)
