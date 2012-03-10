# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


def register(cls, admin_cls):
    cls.add_to_class(
        'last_topic',
        models.ForeignKey(
            'Topic',
        ),
    )
    cls.add_to_class(
        'forum_signature',
        models.CharField(
            max_length=255,
            blank=True,
        ),
    )
    cls.add_to_class(
        'rank',
        models.CharField(
            max_length=20,
            choice=RANK_CHOICE,
        ),
    )

    if admin_cls:
        if admin_cls.fields:
            admin_cls.fields.append((_('Forum Profile Information'),
                {'fields': ('last_topic', 'forum_signature','rank'),
                'classes': ('collapse'),
                })
            )


