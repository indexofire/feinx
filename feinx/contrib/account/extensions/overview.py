# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


GENDER_CHOICES = (
    (1, _('Male')),
    (2, _('Female')),
    (3, _('Unknown')),
)

def register(cls, admin_cls):
    """
    User basic information
    """
    cls.add_to_class(
        'user',
        models.OneToOneField(
            User,
            unique=True,
            verbose_name=_('user'),
            related_name='profile',
            blank=True,
            null=True,
        )
    )
    cls.add_to_class(
        'gender',
        models.PositiveSmallIntegerField(
            _('Gender'),
            blank=True,
            default=3,
            choices=GENDER_CHOICES,
        )
    )
    cls.add_to_class(
        'birthday',
        models.DateField(
            _('Birthday'),
            blank=True,
            null=True,
        )
    )
    cls.add_to_class(
        'telephone',
        models.CharField(
            _("Telephone Number"),
            blank=True,
            max_length=25,
        )
    )
    cls.add_to_class(
        'mobile',
        models.CharField(
            _("Cell Phone Number"),
            blank=True,
            max_length=15,
        )
    )

    if admin_cls:
        if admin_cls.fieldsets:
            admin_cls.fieldsets.append((_('Overview'),
                {'fields': (
                    #'user',
                    'gender',
                    'birthday',
                    'telephone',
                    'mobile',
                    ),
                'classes': (
                    'collapse',
                    )
                })
            )
