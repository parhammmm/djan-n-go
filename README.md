#djan-n-go

## Introduction
A simple tool for creating a new boilerplate django project (with virtualenv, git, backbone, AMD loader, bootstrap, ...) and replicating a current django project together with its dependencies.

Currently only supports Linux

## Dependencies
You need python2.7, pip and git installed

## Installation

	sudo pip install -e git+https://github.com/skinnyp/djan-n-go.git#egg=Package

## Usage

### To create a new project 

    djan-n-go.py init 

or if you prefere to pass the arguments directly:

	djan-n-go.py init -n name_of_the_project -b project_directory

### To clone an existing project 
	
	djan-n-go.py clone

or if you prefere to pass the arguments directly:

	djan-n-go.py clone -n name_of_the_project -b project_directory -r repository_address

Once you have your project, you must configure django's settings change settings/common.py for development. You also have settings/development.py and settings/production.py settings in the same folder.

## Some notes
* Django's manage.py has been altered to force all new apps to be placed in ./apps

* You must activate the virtualenv (in ./virtualenv) for the project before using manage.py or django-admin.py

* You should add your project's dependencies to the requirements.txt so that it can be cloned with ease in the future

That's it!

## Author & Acknowledgments
Author: Parham <http://parha.me>

Directory layout inspired by:
<http://blog.zacharyvoase.com/2010/02/03/django-project-conventions>

bootstrap <https://github.com/twitter/bootstrap>
backbone-boilerplate <https://github.com/tbranyen/backbone-boilerplate>