# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from feinx.apps.forum.views import *


urlpatterns = patterns('',
    # landing page of a forum
    url(r'^$',
        ForumIndexView.as_view(),
        name='forum-index',
    ),
    # topic list of a forum
    url(r'^forum/(?P<forum_id>\w+)/$',
        ForumForumView.as_view(),
        name='forum-forum',
    ),
    # topic page
    url(r'topic/(?P<topic_id>\d+)/$',
        ForumTopicView.as_view(),
        name='forum-topic',
    ),
    # post new topic
    url(r'topic/new/(?P<forum_id>\d+)/$',
        ForumPostView.as_view(),
        name='forum-post-topic',
    ),
    # post new reply
    url(r'reply/new/(?P<topic_id>\d+)/$',
        ForumPostView.as_view(),
        name='forum-reply-topic',
    ),
    # edit a topic or a reply
    url(r'topic/edit/(?P<post_id>\d+)/$',
        ForumPostView.as_view(),
        name='forum-edit-post',
    ),
    # del a topic or a reply
    url(r'topic/del/(?P<post_id>\d+)/$',
        ForumDeleteView.as_view(),
        name='forum-del-post',
    ),
)

# old function views
#urlpatterns = patterns('',
    #url(r'^$', forum_index, name='forum-index'),
    #url(r'^forum/(?P<forum_slug>\w+)/$', forum_forum, name='forum-forum'),
    #url(r'^topic/(?P<topic_id>\d+)/$', forum_topic, name='forum-topic'),
    #url(r'^topic/new/(?P<forum_id>\d+)/$', 'forum_post_thread', name='forum-post-topic'),
    #url(r'^reply/new/(?P<topic_id>\d+)/$', 'forum_post_thread', name='forum-post-replay'),
    #url(r'^thread/(?P<post_id>\d+)/edit/$', edit_post, name='forum-post-edit'),
    #url(r'^user/(?P<user_id>\d+)/topics/$', user_topics, name='forum-user-topics'),
    #url(r'^user/(?P<user_id>\d+)/posts/$', user_posts, name='forum-user-posts'),
    #url('^markitup_preview/$', markitup_preview, name='markitup-preview'),
#)
