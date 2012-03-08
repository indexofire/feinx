#!/usr/bin/env python
import os
from setuptools import setup, find_packages
from setuptools.dist import Distribution
import pkg_resources

add_django_dependency = True

try:
    pkg_resources.get_distribution('Django')
    add_django_dependency = False
except pkg_resources.DistributionNotFound:
    try:
        import django
        if django.VERSION[0] >= 1 and django.VERSION[1] >= 3 and django.VERSION[2] >= 0:
            add_django_dependency = False
    except ImportError:
        pass

Distribution(
    {"setup_requires": add_django_dependency and  ['Django >=1.3.0'] or []}
)

import feinx

setup(name='FeinX',
    version=feinx.__version__,
    description='Django-based Page CMS and CMS building toolkit.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author='Mark Renton',
    author_email='indexofire@gmail.com',
    url='http://github.com/indexofire/feinx/',
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=[
        'Django >=1.3.0'
    ],
    requires=[
        'django_mptt (>0.5.0)',
    ],
    packages=[
        'feinx',
        'feinx.contrib.profile',
        'feinx.content.markup',
        'feinx.extension.auth',
    ],
    include_package_data=True,
    zip_safe=False,
)
