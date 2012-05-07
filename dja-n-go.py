#!/usr/bin/env python

import sys
import os
import re
import platform
import subprocess
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', help='project name')
parser.add_argument('-b', '--base_path', help='the base path for the project')
args = parser.parse_args()

# The package names in pypi for requriments in the project
default_requirements = ['django']

# The list of files and folders to include in the .gitignore configuration
to_gitignore = ['virtualenv/**', '*.log', '*.pot', '*.pyc', '*.db']

def is_installed(package_name):
	""" Check to see if a pip package is installed system wide """
	p = subprocess.Popen(['pip', 'freeze'], stdout=subprocess.PIPE)

	for package in p.communicate()[0].split("\n"):
		if str(package).split("==")[0] == package_name:
			return True

	return False

def read_input(message):
	""" Read none empty stdin with no new line at the end """
	input = raw_input(message)
	if input is "":
		print "\tNothing entered"
		read_input(message)
	else:
		return input

def bin_dir(path):
	""" Get the bin directory for the virtualenv with respect to the OS """
	if platform.system() == "Windows":
		bin_path = os.path.join(path, 'virtualenv', 'Scripts')
	else:
		bin_path = os.path.join(path, 'virtualenv', 'bin')

	return bin_path

def dir_setup(path):
	""" Create an empty project directory """
	if not os.path.isdir(path):
		os.makedirs(path)
		return path
	else:
		sys.exit("\tError: '"+path+"' invalid or already in use choose another")

def vitualenv_setup(path):
	""" Set up a new virtualenv in the project directory """
	# If virtualenv isn't installed install it
	if not is_installed("virtualenv"):
		subprocess.call(['pip', 'install', 'virtualenv'])

	subprocess.call(['virtualenv', 'virtualenv'])

	# path for virtualenv
	return os.path.join(path, 'virtualenv')

def setup_git(path):
	gitignore = open(os.path.join(path, '.gitignore'), 'w+')
	gitignore.write('\n'.join(to_gitignore))
	gitignore.close()

	subprocess.call(['git', 'init'])
	subprocess.call(['git', 'add', '.'])
	subprocess.call(['git', 'commit', '-m', 'First Commit'])

def configure_django(name, path, template_path):
	print('\t>>> Configuring Django...')
	os.system(os.path.join(bin_dir(path), 'activate')+' && python '+os.path.join(bin_dir(path), 'django-admin.py')+' startproject --template='+template_path+' '+name+' '+path)

def setup_requirements(path, default_requirements):
	f = open(os.path.join(path, 'requirements.txt'), 'w+')
	f.write('\n'.join(default_requirements))
	f.close()

	os.system(os.path.join(bin_dir(path), 'activate')+' && '+ os.path.join(bin_dir(path), 'pip') + ' install -r' + os.path.join(path, 'requirements.txt'))

def main():
	if not platform.system() == "Windows" and not platform.system() == "Linux":
		sys.exit('\tError: Unsupported OS')

	script_path = os.path.dirname(os.path.realpath(__file__))

	if args.name is None or args.base_path is None:
		print("Project Setup")
		print("-------------")
		name = read_input("Name: ")
		base_path = read_input("Base Path (. for current directory): ")
	else:
		name = args.name
		base_path = args.base_path

	# Check to see if valid django project name (from django's source)
	if not re.search(r'^[_a-zA-Z]\w*$', name):
		if not re.search(r'^[_a-zA-Z]', name):
			message = ('make sure the name begins with a letter or underscore')
		else:
			message = 'use only numbers, letters and underscores'
		exit("%r is not a valid project name. Please %s." % (name, message))

	# The root directory of the project
	path = os.path.join(os.path.abspath(base_path), name)

	print('>>> Setting up the dirs...')
	dir_setup(path)
	os.chdir(path)

	print('>>> Setting up the virtualenv...')
	vitualenv_setup(path)

	print('>>> Installing requirements...')
	setup_requirements(path, default_requirements)
	configure_django(name, path, os.path.join(script_path, 'django-template'))

	print('>>> Setting up git...')
	setup_git(path)

if __name__ == '__main__':
	main()