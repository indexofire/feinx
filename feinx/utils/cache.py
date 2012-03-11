# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.cache import cache


CACHE_TIMEOUT = getattr(settings, 'CACHE_TIMEOUT', 60*60*24)
cached_funcs = set()

def get_cache_key(prefix):
    """
    Returns a cache key consisten of a username and image size.
    """
    return '%s' % (prefix)

def cache_result(func):
    """
    Decorator to cache the result of functions.
    """
    def cache_set(key, value):
        cache.set(key, value, CACHE_TIMEOUT)
        return value

    def cached_func():
        prefix = func.__name__
        cached_funcs.add(prefix)
        key = get_cache_key(prefix=prefix)
        return cache.get(key) or cache_set(key, func())
    return cached_func
