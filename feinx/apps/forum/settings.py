# -*- coding: utf-8 -*-
from django.conf import settings


DEFAULT_CTX_CONFIG = {
    'FORUM_TITLE': '',
    'FORUM_SUB_TITLE': '',
    'FORUM_PAGE_SIZE': 10,
    'TOPIC_PAGE_SIZE': 10,
    'AVATAR_HEIGHT': 48,
    'AVATAR_WIDTH': 48,
}

LATEST_TOPIC_NUMBER = getattr(settings, 'LATEST_TOPIC_NUMBER', 10)
