# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from feinx.contrib.profile.models import Profile, ProfileAdmin

#class ProfileInline(admin.StackedInline):
#    model = Profile
#    fk_name = 'user'
#    can_delete = False
#    max_num = 1
#    verbose_name_plural = _('profile')

#class UserAdmin(UserAdmin):
#    inlines = (ProfileInline, )

admin.site.unregister(User)
#admin.site.register(User, UserAdmin)

admin.site.register(Profile, ProfileAdmin)
