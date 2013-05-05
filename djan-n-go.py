#!/usr/bin/env python

import sys
import os
import re
import platform
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('action', metavar="action", type=str, choices=['init'], help="Init a new project")
parser.add_argument('-n', '--name', metavar="project name", help='Name of the new project')
parser.add_argument('-b', '--base_path', metavar="project folder", help='Base path for the project')
args = parser.parse_args()

# The package names in pypi for requriments in the project
default_requirements = [
	'django', 
	'south', 
	'ssh', 
	'fabric', 
	'pytz',
	'boto', 
	'django-storages',
	'django-pipeline',
]

# The list of files and folders to include in the .gitignore configuration
to_gitignore = [
	'virtualenv/**', 
	'*.log', 
	'*.pot', 
	'*.pyc', 
	'*.db', 
	'*.swp', 
	'*.swo',
]

def is_installed(package_name):
	""" Check to see if a pip package is installed system wide """
	p = subprocess.Popen(['pip', 'freeze'], stdout=subprocess.PIPE)

	for package in p.communicate()[0].split("\n"):
		if str(package).split("==")[0] == package_name:
			return True

	return False

def project_init(name, base_path):
	# The root directory of the project
	path = os.path.join(os.path.abspath(base_path), name)

	script_path = os.path.dirname(os.path.realpath(__file__))
	template_path = os.path.join(script_path, 'django-template')

	print('>>> Setting up the dirs...')
	# Create an empty project directory
	if not os.path.isdir(path):
		os.makedirs(path)
	else:
		sys.exit("\tError: %s invalid or already in use choose another" % path)

	os.chdir(path)

	# Build the requirements file
	f = open(os.path.join(path, 'requirements.txt'), 'w+')
	f.write('\n'.join(default_requirements))
	f.close()

	#print('>>> Installing PIP...')
	os.system('sudo curl http://python-distribute.org/distribute_setup.py | python')
	os.system('sudo curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python')

	print('>>> Installing Django...')
	os.system('pip install django')

	print('\t>>> Configuring Django...')
	# Use the provided django template to start off the project
	os.system('django-admin.py startproject --template=%s %s %s' % (template_path, name, path))

	print('\t>>> Installing Dependencies...')
	os.chdir(os.path.join(path, 'bin/'))
	subprocess.call(['sudo', 'chmod', 'u+x', 'install.sh']) 
	subprocess.call(['sudo', './install.sh']) 
	os.chdir(path)

	print('>>> Setting up git...')
	gitignore = open(os.path.join(path, '.gitignore'), 'w+')
	gitignore.write('\n'.join(to_gitignore))
	gitignore.close()

	subprocess.call(['git', 'init'])
	subprocess.call(['git', 'add', '.'])
	subprocess.call(['git', 'commit', '-m', 'First Commit'])

def project_check_name(name):
	# Check to see if valid django project name (from django's source)
	if not re.search(r'^[_a-zA-Z]\w*$', name):
		if not re.search(r'^[_a-zA-Z]', name):
			message = ('make sure the name begins with a letter or underscore')
		else:
			message = 'use only numbers, letters and underscores'
		exit("%r is not a valid project name. Please %s." % (name, message))

def read_input(message):
	""" Read none empty stdin with no new line at the end """
	input = raw_input(message)
	if input is "":
		print "\tNothing entered"
		read_input(message)
	else:
		return input

def main():
	if not platform.system() == "Linux":
		sys.exit('\tError: Unsupported OS')

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
