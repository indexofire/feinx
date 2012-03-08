# -*- coding: utf-8 -*-
import socket
from random import choice
from os.path import dirname, abspath, normpath, basename, join
from django.utils.importlib import import_module


PROJECT_PATH = normpath(dirname(dirname(dirname(abspath(__file__)))))
PROJECT_NAME = basename(PROJECT_PATH)

# write your own settings split type here. do not write same settings name
# here in different setting type.
HOST_MAP = {
    'settings_dev': (
        'mark-desktop',
        'my-computer',
        'markmatoMacBook-Air.local',
    ),
    'settings_vps': (
        'django-server',
        'hzcdclabs.org',
    ),
    'settings_epio': (
        'ep.io',
    ),
    'settings_dotcloud': (
        'dotcloud.com',
    ),
}
CURRENT_HOST = socket.gethostname()
DISPATCHER = []
KEY_CHAR= 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

def update_settings(s):
    """
    Updating settings via using a settings filename as a settings. This
    function will insert all variables and functions in ALL_CAPS into the
    global scope.
    """
    settings = import_module('%s.settings.%s' % (PROJECT_NAME, s))
    for k, v in settings.__dict__.items():
        if k.upper() == k:
            globals().update({k:v})

def create_secret_key(key_file, char=KEY_CHAR):
    """
    Create your own django project secret key.
    """
    try:
        f = open(key_file)
        key = f.read().strip()
        if len(key) == 50:
            return key
        else:
            return f.write(''.join([choice(KEY_CHAR) for i in range(50)]))
    except IOError:
        try:
            with open(key_file, 'w') as f:
                f.write(''.join([choice(KEY_CHAR) for i in range(50)]))
        except IOError:
            raise Exception('Can not open file `%s` for writing.' % key_file)
    finally:
        if f:
            f.close()

for k, v in HOST_MAP.items():
    for h in v:
        if CURRENT_HOST == h:
            DISPATCHER.append(k)

for settings in DISPATCHER:
    try:
        update_settings(settings)
    except ImportError:
        print "Error import %s" % settings
