#! /usr/bin/python
# run this line to install teh packages [ python setup.py sdist ]
from setuptools import setup, find_packages

setup(
    name='pybrainframework',
    vesrion='0.0.1',
    auther='Hytham Alobydi',
    auther_email='haiwa80@biomedicallc.net',
    description='This is a simple library that will allway to create a graph of networks',
    packages=find_packages()
)
