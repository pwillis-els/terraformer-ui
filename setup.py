#!/usr/bin/env python

import codecs
from os import path
from platform import system

from setuptools import setup

with open('requirements.txt') as f:
    install_requires = f.readlines()

VERSION = "0.0.5"

setup(
    name        =  'terraformer-ui',
    packages    = ['terraformer_ui'],
    version     =   VERSION,
    description =  'User Interface to Terraformer',
    url         =  'https://github.com/pwillis-els/terraformer-ui.git',

    install_requires=install_requires,

    long_description=codecs.open(
        path.join(path.abspath(path.dirname(__file__)), 'README.md'),
        mode='r', encoding='utf-8'
    ).read(),


    setup_requires=[
        'setuptools',
    ],

    entry_points={
        'console_scripts': ['terraformer-ui=terraformer_ui.console:main']
    },

    #package_data={'terraformer-ui': ['data/*']},
    include_package_data=True,
    data_files = [ ( 'data', ['terraformer_ui/data/resources.yaml'] ) ],

    python_requires='>=3.5'
)
