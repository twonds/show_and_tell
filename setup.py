#!/usr/bin/env python

from distutils.core import setup

setup(name='show_and_tell',
      version='1.0',
      description='Interactive command line demos',
      author='Christopher Zorn',
      author_email='christopher.zorn@gmail.com',
      depends=['pyyaml'],
      scripts=['scripts/show_and_tell'],
      packages=['show_and_tell'],
     )
