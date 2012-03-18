# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from feinx.apps.forum.models import *

def update_topic_num_replies(modeladmin, request, queryset):
    for topic in queryset:
        topic.num_replies = topic.count_nums_replies()
        topic.save()
update_topic_num_replies.short_description = _(u"Update replies numbers")

def update_forum_nums_topic_post(modeladmin, request, queryset):
    for forum in queryset:
        forum.num_topics = forum.count_nums_topic()
        forum.num_posts = forum.count_nums_post()
        if forum.num_topics:
            forum.last_post = forum.topic_set.order_by('-last_reply_on')[0].last_post
        else:
            forum.last_post = ''
        forum.save()
update_forum_nums_topic_post.short_description = _(u"Update topic/post numbers")

class ForumAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'get_topic_number',
        'get_thread_number',
    )
    actions = [update_forum_nums_topic_post]


class ReplyInline(admin.TabularInline):
    model = Reply

class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'forum',
        'author',
        'sticky',
        'closed',
        'hidden',
        'view_num',
        'reply_num',
        'created',
        'updated',
    )
    list_filter = ('forum', 'sticky', 'closed', 'hidden',)
    search_fields = ('subject', 'author__username', )
    inlines = (ReplyInline, )
    actions = [update_topic_num_replies]


class ReplyAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'topic',
        'author',
        'author_ip',
        'created',
        'updated',
    )
    search_fields = ('topic__subject', 'author__username', 'message', )


admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Reply, ReplyAdmin)
