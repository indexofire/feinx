# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.admin import UserAdmin, csrf_protect_m
from django.utils.translation import ugettext_lazy as _
from feinx.contrib.account.forms import ProfileAdminForm
from feinx.utils.mixins import ExtensionMixin


if getattr(settings, 'AUTH_PROFILE_MODULE', False) and settings.AUTH_PROFILE_MODULE == "profile.Profile":
    def get_profile(self):
        """Returns profile for this user."""
        return self.profile
    User.get_profile = get_profile

class ProfileAdmin(UserAdmin):
    """
    Profile admin class inherit from UserAdmin.

    UserAdmin.get_fieldsets(self, request, obj=None)
    UserAdmin.get_form(self, request, obj=None, **kwargs)
    UserAdmin.get_urls(self)
    UserAdmin.add_view(self, request, form_url='', extra_context=None)
    UserAdmin.user_change_password(self, request, id, form_url='')
    UserAdmin.response_add(self, request, obj, post_url_continue='../%s/')

    UserAdmin.fields:
        form
        add_form_template
        change_user_password_template
        fieldsets
        add_fieldsets
        add_form
        change_password_form
        list_display
        list_filter
        search_fields
        ordering
        filter_horizontal
    """

    form = ProfileAdminForm
    #add_form_template = None
    fieldsets = [
        (_('Main options'), {
            'fields': ['username', 'password', 'email',],
        }),
        (_('Other options'), {
            'classes': ['wide',],
            'fields': ['is_active', 'last_login', 'date_joined',],
        }),
    ]
    list_display = ['username', 'email', 'date_joined',]
    list_display_links = ['username', 'email',]
    list_display_filter = []
    list_filter = ['is_active', 'date_joined', 'last_login',]
    search_fields = ['username', 'email',]
    readonly_fields = ['last_login', 'date_joined', ]
    ordering = ('username', 'username', 'email',)

    def get_fieldsets(self, request, obj=None):
        # Override the UserAdmin add view and return it's parent.
        return super(UserAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """If this is an add then remove the password help_text."""
        # Override the UserAdmin add view and return it's parent.
        form = super(UserAdmin, self).get_form(request, obj=obj, **kwargs)
        if obj is None:
            form.base_fields['password'].help_text = ''
        form.base_fields['username'].required = True
        #form.base_fields['email'].required = True
        #form.base_fields['first_name'].required = True
        #form.base_fields['last_name'].required = True
        return form

    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, **kwargs):
        # Override the UserAdmin add view and return it's parent.
        return super(UserAdmin, self).add_view(request, **kwargs)

    def save_form(self, request, form, change):
        """If this is an add then set the password."""
        user = super(ProfileAdmin, self).save_form(request, form, change)
        if not change and user.password:
            user.set_password(user.password)
        return user

class ProfileManager(UserManager):
    """
    Objects manager for custom profile.
    """
    pass

class Profile(User, ExtensionMixin):
    """
    User profile models for import other extensions
    """
    objects = ProfileManager()
    _extensions_imported = False
    _admin = ProfileAdmin

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

    def get_full_name(self):
        full_name = super(Profile, self).get_full_name()
        if not full_name:
            return self.username
        return full_name

    def get_profile(self):
        return self



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Post a signal to create a matching profile when a user object is created.
    """
    if created:
        profile, new = Profile.objects.get_or_create(id=instance.pk)

# Register extensions listed in the settings
PROFILE_EXTENSIONS = getattr(settings, 'PROFILE_EXTENSIONS', None)

if PROFILE_EXTENSIONS and not Profile._extensions_imported:
    Profile.register_extensions(*PROFILE_EXTENSIONS)
    Profile._extensions_imported = True
