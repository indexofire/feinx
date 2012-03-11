# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


def register(cls, admin_cls):
    """
    User portifolio.
    """
    GENDER_CHOICES = (
        (1, _('Male')),
        (2, _('Female')),
        (3, _('Unknown')),
    )
    # field for people's nickname
    cls.add_to_class(
        models.CharField(
            _('Nickname'),
            blank=True,
            max_length=50,
            help_text=_('Name display in site')
        )
    )
    # field for people's sex
    cls.add_to_class(
        'gender',
        models.PositiveSmallIntegerField(
            _('Gender'),
            blank=True,
            default=3,
            choices=GENDER_CHOICES,
        )
    )
    # field for people's date of birth
    cls.add_to_class(
        'birthday',
        models.DateField(
            _('Birthday'),
            blank=True,
        )
    )
    # field for user's telephone number
    cls.add_to_class(
        'telephone',
        models.CharField(
            _("Telephone Number"),
            blank=True,
            max_length=25,
        )
    )
    # field for user's mobile number
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
            admin_cls.fieldsets.append((
                _('Overview'), {
                    'fields': (
                        'gender',
                        'birthday',
                        'telephone',
                        'mobile',
                        ),
                    'classes': (
                        'collapse',
                        )
                    }
                )
            )
