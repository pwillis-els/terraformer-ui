#!/usr/bin/env python

import codecs
from os import path
from platform import system

from setuptools import setup

with open('requirements.txt') as f:
    install_requires = f.readlines()

VERSION = "2020-08-28"

setup(
    name='terraformer-ui',
    version=VERSION,
    description='User Interface to Terraformer',

    install_requires=install_requires,

    long_description=codecs.open(
        path.join(path.abspath(path.dirname(__file__)), 'README.md'),
        mode='r',
        encoding='utf-8'
    ).read(),

    url='https://github.com/pwillis-els/terraformer-ui.git',
    packages=['terraformer_ui'],
    setup_requires=[
        'setuptools',
    ],
    entry_points={
        'console_scripts': ['terraformer-ui=terraformer_ui.console:main']
    },
    include_package_data=True,
    python_requires='>=3.5'
)
