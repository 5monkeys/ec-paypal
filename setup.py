#!/usr/bin/env python
from setuptools import setup, find_packages

name = 'ec_paypal'

setup(
    name=name,
    version=__import__(name).__version__,
    packages=find_packages(exclude=['_*']),
    install_requires=['requests'],
)
