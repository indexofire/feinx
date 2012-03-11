# -*- coding: utf-8 -*-
from feinx.contrib.account.models import Profile

class ProfileAuthenticationMiddleware(object):
    """
    Replace authentication middleware

    Usage:
        MIDDLEWARE_CLASSES = (
            ...
            #'django.contrib.auth.middleware.AuthenticationMiddleware',
            'feinx.contrib.profile.middleware.ProfileAuthenticationMiddleware',
            ...
        )
    """
    def process_request(self, request):
        request.__class__.user = Profile()
        return None
