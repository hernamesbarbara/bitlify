#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import re 

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def find_version(fname):
    '''Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    '''
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version

__version__ = find_version("bin/bitlify")

config = {
    'description': 'shorten urls using bitly from command line',
    'author': 'austin',
    'keywords': 'shorten urls, bitly, CLI',
    'author_email': 'tips@cia.lol',
    'version': __version__,
    'install_requires': ['docopt', 'requests', 'pandas'],
    'packages': ['bitlyutils'],
    'include_package_data': True,
    'scripts': ['bin/bitlify'],
    'zip_safe': False,
    'name': 'bitlify',
    'license': 'MIT'
}

setup(**config)