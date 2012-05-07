#!/usr/bin/env python

from distutils.core import setup
import os


template_dir = os.path.abspath('django-template')

data_files = []

for dirpath, dirnames, filenames in os.walk(template_dir):
    if filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup (
    name='djan-n-go',
    version='0.0.1',
    description='Plain django with all the goodies included',
    long_description=open('README').read(),
    author='Parham Saidi',
    author_email='parham@parha.me',
    url='https://github.com/skinnyp/djan-n-go',
    data_files = data_files,
    scripts = ['djan-n-go.py'],
    license='BSD',
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    )
)