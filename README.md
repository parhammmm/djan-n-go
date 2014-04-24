#djan-n-go

## Introduction
Automation of repetative tasks used when creating a new django project.

Currently only used on Linux

## Installation

	sudo pip install -e git+https://github.com/skinnyp/djan-n-go.git#egg=Package

## Usage

### To create a new project 

    djan-n-go.py init 

or if you prefere to pass the arguments directly:

	djan-n-go.py init -n name_of_the_project -b project_directory

Once you have your project, you must configure django's settings change settings/common.py for development. 
You also have settings/development.py and settings/production.py settings in the same folder, which must be modified for fabric tasks.

## Fabric Tasks

 * deploy
 * deploy_admin_static
 * deploy_static
 * initial_setup
 * staging
 * production

## Author & Acknowledgments
Author: Parham <http://parha.me>

Directory layout inspired by:
<http://blog.zacharyvoase.com/2010/02/03/django-project-conventions>

bootstrap <https://github.com/twitter/bootstrap>
backbone-boilerplate <https://github.com/tbranyen/backbone-boilerplate>
