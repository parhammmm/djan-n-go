# Copyright 2012 Parham Saidi. All rights reserved.

import string
import random

def random_string_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))
