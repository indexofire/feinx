# -*- coding: utf-8 -*-
from django.conf import settings
from .settings import DEFAULT_CTX_CONFIG


def forum(request):
    ctx_extras = getattr(settings, 'FORUM_CTX_CONFIG', DEFAULT_CTX_CONFIG)
    return ctx_extras
