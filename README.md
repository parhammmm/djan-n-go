#djan-n-go

## Introduction
A simple tool for creating a new django project (and all the goodies e.g. 
virtualenv, git, bootstrap, h5bp, ...), with a customised directory layout.

Currently tested on Windows and Linux. If you're a mac user take off
the platform.system() check in main() and let me know if it works :)

## Installation
	pip install -e git+https://github.com/skinnyp/djan-n-go.git#egg=Package

## Usage
	djan-n-go.py -n name_of_the_project -b project_root_directory

or follow the onscreen prompts:

	djan-n-go.py

## Some notes
* Django's manage.py has been altered to force all new apps to be placed in ./apps

* You must activate the virtualenv (in ./virtualenv) for the project before using manage.py or django-admin.py

That's it!

## Author & Acknowledgments
Author: Parham <parham [ a t ] parha.me>

Directory layout inspired by:
	
		http://blog.zacharyvoase.com/2010/02/03/django-project-conventions/