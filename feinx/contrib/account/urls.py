# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from feinx.contrib.account.views import ProfileView, ProfileEdit


urlpatterns = patterns('',
    url(r'^$',
        ProfileView.as_view(),
        name='profile-index',
    ),
    url(r'^profile/(?P<username>\w+)/$',
        ProfileView.as_view(),
        name='profile-detail',
    ),
    url(r'^profile/(?P<username>\w+)/edit/$',
        ProfileEdit.as_view(),
        name='profile-edit',
    ),
)
