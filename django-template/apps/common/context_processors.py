# Copyright 2012 Parham Saidi. All rights reserved.

from django.conf import settings

def debug_mode(request):
	return {'debug_mode': settings.DEBUG}

def is_production(request):
	return {'is_production': settings.IS_PRODUCTION}
