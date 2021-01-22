# -*- coding: utf-8 -*-

import re
from pathlib import Path
from setuptools import setup


def read(fname):
    return Path(__file__).resolve().parent.joinpath(fname).open().read()


version = re.search(
        r'^__version__\s*=\s*"(.*)"',
        open('texbrix/texbrix.py').read(),
        re.M
        ).group(1)

setup(
    name="TeXBriX",
    version=version,
    packages=["texbrix"],
    include_package_data=True,
    entry_points={
        "console_scripts": ['texbrix=texbrix.texbrix:main']
    },
    author="Leopold Fajtak",
    author_email="leopold@fajtak.at",
    description="A granular approach to LaTeX",
    license="GPLv3",
    keywords="mathematics dependencies layout filestructure",
    url="http://github.com/leopoldfajtak/texbrix",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing :: Markup :: LaTeX"
        ]
)
