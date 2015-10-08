#!/usr/bin/env python

import subprocess
import shlex
from setuptools import setup


version = '0.1.0.0'

try:
    hash = (
        subprocess
        .check_output(shlex.split('git rev-parse --short HEAD'))
        .rstrip()
        .decode('ASCII')
    )
    commit = (
        subprocess
        .check_output(shlex.split('git rev-list --count HEAD'))
        .rstrip()
        .decode('ASCII')
    )
except:
    pass
else:
    version = '{}.dev{}+{}'.format(version, commit, hash)


setup(
    name='silly-words',
    version=version,
    description=(
        "A template API to generate silly words from abstract templates."
    ),
    author="Sebastian Reuße",
    author_email='seb@wirrsal.net',
    url='https://github.com/eigengrau/silly-words',
    install_requires=[
        'nltk >=3.0, <=3.1',
        'pyparsing >=2.0, <=2.1'
    ],
    packages=['silly_words'],
    package_dir={'': 'src'},
    license="GPL3",
    entry_points={
        'console_scripts': [
            'silly-words = silly_words.cli:console_entry',
        ]
    }
)
