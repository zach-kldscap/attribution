#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

setup(
    name='Attribution',
    version='0.0.1',
    description='Attribution Framework',
    author='Zach Dingels',
    author_email='zach.dingels@kldscap.com',
    url='na',
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
