# !/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.md') as f:
    readme = f.read()

setup(
    name='primestatsbot',
    version='2.0.0',
    description='This is a simple Telegram handlers for converting exported stats'
                ' from Ingress Prime to a nicely formatted message.',
    long_description=readme,
    author='Pascal Roose',
    author_email='pascalroose@outlook.com',
    url='https://github.com/PascalRoose/primestatsbot',
    packages=['primestatsbot']
)
