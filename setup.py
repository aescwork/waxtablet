# -*- coding: utf-8 -*-


# Always prefer setuptools over distutils

import os
import sys
import errno

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

# To use a consistent encoding

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='waxtablet',
    version='1.0',
    description='A command-line journaling application which stores text entries in a database and displays them in html.',
    long_description=long_description,
    url='https://github.com/aescwork/waxtablet',
    author='aescwork',
    author_email='aescwork@protonmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='journal diary database text log organizer organization',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    entry_points={
        'console_scripts': [
            'waxtablet=waxtablet.main:main',
        ],
    },
)


