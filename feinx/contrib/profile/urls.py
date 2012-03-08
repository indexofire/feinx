# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from contrib.profile.views import ProfileView, ProfileEdit


urlpatterns = patterns('',
    url(r'^$', ProfileView.as_view(), name='profile-index'),
    url(r'^edit/$', ProfileEdit.as_view(), name='profile-edit'),
)
