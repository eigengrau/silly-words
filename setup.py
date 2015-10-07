#!/usr/bin/env python

import subprocess
import shlex
from setuptools import setup


try:
    revision = (
        subprocess
        .check_output(shlex.split('git rev-parse --short HEAD'))
        .rstrip()
        .decode('ASCII')
    )
except:
    revision = '0.1.0.0'


setup(
    name='silly-words',
    version=revision,
    description=(
        "A template API to generate silly words from abstract templates."
    ),
    author="Sebastian Reuße",
    author_email='seb@wirrsal.net',
    url='https://github.com/eigengrau/silly-words',
    packages=['silly_words'],
    package_dir={'': 'src'},
    license="GPL3",
    entry_points={
        'console_scripts': [
            'silly-words = silly_words.cli:console_entry',
        ]
    }
)
