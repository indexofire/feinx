# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import get_callable
#from django.db.models import get_model

class ProfileModelBackend(ModelBackend):
    """
    Profile model backe nd

    Usage:
        Put these lines in your settings.py file

        AUTHENTICATION_BACKENDS = (
            'feinx.contrib.profile.auth_backends.ProfileModelBackend',
        )
        CUSTOM_USER_MODEL = 'feinx.contrib.profile.models.Profile'
    """

    def authenticate(self, username=None, password=None):
        try:
            user = self.user_class.objects.get(username=username)
            if user.check_password(password):
                return user
        except self.user_class.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None

    @property
    def user_class(self):
        if not hasattr(self, '_user_class'):
            self._user_class = get_callable(settings.CUSTOM_USER_MODEL, False)
            if self._user_class is False:
                raise ImproperlyConfigured(_('Could not get custom user model'))
        return self._user_class
