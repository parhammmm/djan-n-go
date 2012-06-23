#!/usr/bin/env python

import sys
import os
import re
import platform
import subprocess
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('action', metavar="action", type=str, choices=['init', 'clone'], help="Init a new project or clone an existing one")
parser.add_argument('-n', '--name', metavar="project name", help='The name of the new project')
parser.add_argument('-b', '--base_path', metavar="project folder", help='The base path for the project')
parser.add_argument('-r', '--repo', metavar="project repository", help='The path to the project repository')
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

def get_bin_dir(path):
	return os.path.join(path, 'virtualenv', 'bin')

def read_input(message):
	""" Read none empty stdin with no new line at the end """
	input = raw_input(message)
	if input is "":
		print "\tNothing entered"
		read_input(message)
	else:
		return input

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
		subprocess.call(['sudo', 'pip', 'install', 'virtualenv'])

	subprocess.call(['virtualenv', 'virtualenv'])

	# path for virtualenv
	return os.path.join(path, 'virtualenv')

def virtualenv_activate(path):
	activate_path = os.path.join(get_bin_dir(path), 'activate_this.py')
	execfile(activate_path, dict(__file__=activate_path)) 

def git_init(path):
	gitignore = open(os.path.join(path, '.gitignore'), 'w+')
	gitignore.write('\n'.join(to_gitignore))
	gitignore.close()

	subprocess.call(['git', 'init'])
	subprocess.call(['git', 'add', '.'])
	subprocess.call(['git', 'commit', '-m', 'First Commit'])

def git_clone(path, repo):
	subprocess.call(['git', 'clone', repo, path])

def django_configure(path, name, template_path):
	print('\t>>> Configuring Django...')
	os.system(os.path.join(get_bin_dir(path), 'django-admin.py')+' startproject --template='+template_path+' '+name+' '+path)

def requirements_set_file(path, default_requirements):
	f = open(os.path.join(path, 'requirements.txt'), 'w+')
	f.write('\n'.join(default_requirements))
	f.close()
	requirements_install(path)

def requirements_install(path):
	os.system(os.path.join(get_bin_dir(path), 'pip') + ' install -r ' + os.path.join(path, 'requirements.txt'))

def project_init(name, base_path):
	script_path = os.path.dirname(os.path.realpath(__file__))

	# The root directory of the project
	path = os.path.join(os.path.abspath(base_path), name)

	print('>>> Setting up the dirs...')
	dir_setup(path)
	os.chdir(path)

	print('>>> Setting up the virtualenv...')
	vitualenv_setup(path)
	virtualenv_activate(path)

	print('>>> Installing requirements...')
	requirements_set_file(path, default_requirements)
	django_configure(path, name, os.path.join(script_path, 'django-template'))

	print('>>> Setting up git...')
	git_init(path)

def project_clone(name, base_path, repo):
	# The root directory of the project
	path = os.path.join(os.path.abspath(base_path), name)

	print('>>> Cloning project...')
	git_clone(path, repo)

	os.chdir(path)

	print('>>> Setting up the virtualenv...')
	vitualenv_setup(path)
	virtualenv_activate(path)

	print('>>> Installing requirements...')
	requirements_install(path)

def project_check_name(name):
	# Check to see if valid django project name (from django's source)
	if not re.search(r'^[_a-zA-Z]\w*$', name):
		if not re.search(r'^[_a-zA-Z]', name):
			message = ('make sure the name begins with a letter or underscore')
		else:
			message = 'use only numbers, letters and underscores'
		exit("%r is not a valid project name. Please %s." % (name, message))

def main():
	if not platform.system() == "Linux":
		sys.exit('\tError: Unsupported OS')

	if args.action == "clone":
		if args.name is None or args.base_path is None or args.repo is None:
			print("Project Setup")
			print("-------------")
			name = read_input("Name: ")
			project_check_name(name)
			base_path = read_input("Base Path (. for current directory): ")
			repo = read_input("Project repo: ")
		else:
			name = args.name
			base_path = args.base_path
			repo = args.repo
			project_check_name(name)

		project_clone(name, base_path, repo)

	if args.action == "init":
		if args.name is None or args.base_path is None:
			print("Project Setup")
			print("-------------")
			name = read_input("Name: ")
			project_check_name(name)
			base_path = read_input("Base Path (. for current directory): ")
		else:
			name = args.name
			base_path = args.base_path
			project_check_name(name)

		project_init(name, base_path)

if __name__ == '__main__':
	main()