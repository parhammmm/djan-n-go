#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")

	from django.core.management import execute_from_command_line

	# Force all new new apps to be put in the apps directory
	if sys.argv[1] == 'startapp':
		app_path = os.path.join('apps', sys.argv[2])
		os.makedirs(app_path)
		sys.argv.append(app_path)

	execute_from_command_line(sys.argv)