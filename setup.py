#from setuptools import setup

from distutils.core import setup
import py2exe

packages = ['src', 'test']
setup(console=['src/application.py'])
