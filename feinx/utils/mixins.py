# -*- coding: utf-8 -*-
from django.core.urlresolvers import get_callable


class ExtensionMixin(object):
    """
    Mixin for model extensions.
    """

    @classmethod
    def remove_field(cls, f_name):
        """ Removes the field from local fields list """
        cls._meta.local_fields = [f for f in cls._meta.local_fields if f.name != f_name]

        # Removes the field setter if exists
        if hasattr(cls, f_name): delattr(cls, f_name)

    @classmethod
    def register_extension(cls, register_fn):
        """ Register extension """
        register_fn(cls, cls._admin)

    @classmethod
    def register_extensions(cls, *extensions):
        cls_name = '_%s_extensions' % cls.__name__.lower()
        if not hasattr(cls, cls_name):
            setattr(cls, cls_name, set())

        here = cls.__module__.split('.')[:-1]
        here_path = '.'.join(here + ['extensions'])

        for ext in extensions:
            if ext in getattr(cls, cls_name): continue

            try:
                if isinstance(ext, basestring):
                    try:
                        fn = get_callable(ext + '.register', False)
                    except ImportError:
                        fn = get_callable('%s.%s.register' % (here_path, ext), False)
                # Not a string, so take our chances and just try to access "register"
                else:
                    fn = ext.register

                cls.register_extension(fn)
                cls._profile_extensions.add(ext)
            except Exception:
                raise

    @classmethod
    def unregister_extension(cls, unregister_fn):
        """ Unregister extension """
        unregister_fn(cls, cls._admin)
