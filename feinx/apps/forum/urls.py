# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from apps.forum.views import *


urlpatterns = patterns('',
    # landing page of a forum
    url(r'^$', forum_index, name='forum-index'),
    # topic list of a forum
    url(r'^forum/(?P<forum_slug>\w+)/$', forum_forum, name='forum-forum'),
    # topic page
    url(r'^topic/(?P<topic_id>\d+)/$', forum_topic, name='forum-topic'),
    # add new topic
    url(r'^topic/new/(?P<forum_id>\d+)/$', forum_post_thread,
        name='forum-post-topic'),
    # add new reply to a topic
    url(r'^reply/new/(?P<topic_id>\d+)/$', forum_post_thread,
        name='forum-post-replay'),
    #
    url(r'^post/(?P<post_id>\d+)/$', post, name='forum-post'),
    # edit a thread
    url(r'^post/(?P<post_id>\d+)/edit/$', edit_post, name='forum-post-edit'),
    # check all topics of a user
    url(r'^user/(?P<user_id>\d+)/topics/$', user_topics,
        name='forum-user-topics'),
    # check all threads of a user
    url(r'^user/(?P<user_id>\d+)/posts/$', user_posts,
        name='forum-user-posts'),
    # preview a new thread
    url('^markitup_preview/$', markitup_preview, name='markitup-preview'),
)
