# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


RANK_CHOICES = (
    (1, _("Level 1")),
    (2, _("Level 2")),
    (3, _("Level 3")),
)

def register(cls, admin_cls):
    """
    Forum user profile
    """
    cls.add_to_class(
        'forum_signature',
        models.CharField(
            max_length=255,
            blank=True,
            null=False,
        ),
    )
    cls.add_to_class(
        'rank',
        models.PositiveSmallIntegerField(
            max_length=2,
            choices=RANK_CHOICES,
            default=1,
        ),
    )

    if admin_cls:
        if admin_cls.fields:
            admin_cls.fields.append((_('Forum Profile Information'),
                {'fields': ('last_topic', 'forum_signature','rank'),
                'classes': ('collapse'),
                })
            )


