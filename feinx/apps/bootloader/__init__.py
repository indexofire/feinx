# -*- coding: utf-8 -*-
from django.conf import settings

from feinx.apps.bootloader.settings import *


def create_content_types(*args, **kwrags):
    for content in self.contents:
        if isinstance(content['models'], basestring):
            try:
                content['models'] = get_object(content['models'])
            except ImportError:
                raise ImproperlyConfigured, '%s is not a valid content type' % content['model']

            create_content_type(**content)

        else:
            try:
                create_content_type(**content)
            except:
                raise ImproperlyConfigured, 'Your configuration for FEINCMS_PAGE_CONTENTS is invalid!'
