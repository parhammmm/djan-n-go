# Copyright 2012 Parham Saidi. All rights reserved.

from storages.backends.s3boto import S3BotoStorage
from django.conf import settings

class StaticS3BotoStorage(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.S3_STATIC_PATH
        super(StaticS3BotoStorage, self).__init__(*args, **kwargs)

class MediaS3BotoStorage(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.S3_MEDIA_PATH
        super(MediaS3BotoStorage, self).__init__(*args, **kwargs)
