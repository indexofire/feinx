# -*- coding: utf-8 -*-
from base64 import b64encode, b64decode
try:
    import cPickle as pickle
except:
    import pickle

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum

from feincms.content.application.models import app_reverse

from feinx.apps.forum.settings import *
from feinx.apps.forum.managers import TopicManager
from feinx.contrib.account.models import Profile

__all__ = [
    'Forum',
    'Topic',
    'Thread',
    'Post',
]

class Category(models.Model):
    pass

class Forum(models.Model):
    """
    Each forum model contains a series of topics.
    """
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255)
    description = models.TextField(_('Description'), help_text='', blank=True)
    moderators = models.ManyToManyField(Profile, blank=True, null=True, verbose_name=_('Moderators'))
    ordering = models.PositiveIntegerField(_('Ordering'), blank=False, default=1)
    created = models.DateTimeField(_('Created Time'), blank=True, auto_now_add=True, editable=False)
    updated = models.DateTimeField(_('Updated Time'), blank=True, null=True)

    class Meta:
        ordering = ['ordering']
        verbose_name = _("Forum")
        verbose_name_plural = _("Forums")

    def count_nums_topic(self):
        return self.topic_set.all().count()

    def count_nums_post(self):
        return self.topic_set.all().aggregate(Sum('num_replies'))['num_replies__sum'] or 0

    def get_last_post(self):
        if not self.last_post:
            return {}
        return pickle.loads(b64decode(self.last_post))

    @property
    def get_topic_number(self):
        return self.topic_set.all().count()

    @models.permalink
    def get_absolute_url(self):
        return app_reverse('forum-forum', 'feinx.apps.forum.urls', {
            'forum_pk': self.pk,
        })

    def __unicode__(self):
        return self.name


class Topic1(models.Model):
    """
    Topic is the top of a thread.
    """
    forum = models.ForeignKey(Forum, verbose_name=_('Forum'))
    author = models.ForeignKey(Profile)
    author_ip = models.IPAddressField(_('Author\'s IP'), blank=True, default='0.0.0.0')
    subject = models.CharField(max_length=999)
    num_views = models.IntegerField(default=0)
    num_replies = models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True)
    last_reply_on = models.DateTimeField(auto_now_add=True)
    last_post = models.CharField(max_length=255, blank=True)
    closed = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    objects = TopicManager()

    class Meta:
        ordering = ['-last_reply_on']
        get_latest_by = ('created_on')
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")

    def __unicode__(self):
        return self.subject

    def count_nums_replies(self):
        return self.post_set.all().count()

    @models.permalink
    def get_absolute_url(self):
        #return ('forum-topic', (), {'topic_id': self.id})
        return app_reverse('forum-post', 'feinx.apps.forum.urls', kwargs={
            'post_id': self.pk,
        })

    def get_last_post(self):
        if not self.last_post:
            return {}
        return pickle.loads(b64decode(self.last_post))

class Thread(models.Model):
    """ Abstract models of thread which could be a topic or a reply. """
    author = models.ForeignKey(Profile)
    author_ip = models.IPAddressField(_('Author\'s IP'), blank=False, default='0.0.0.0')
    created = models.DateTimeField(_('Created Time'), blank=False, auto_now_add=True, editable=False)
    updated = models.DateTimeField(_('Updated Time'), blank=True, null=True)
    #attachment = models.ManyToManyField(Attachment)

    class Meta:
        abstract = True
        ordering = ['-created']
        get_latest_by = 'created'
        verbose_name = _("Thread")
        verbose_name_plural = _("Threads")

    def __unicode__(self):
        return self.pk

    @models.permalink
    def get_absolute_url(self):
        return app_reverse('forum-post', 'feinx.apps.forum.urls', kwargs={
            'post_id': self.pk,
        })

class Reply(ForumThread):
    """ A reply models of a topic. """
    topic = models.ForeignKey(Topic, verbose_name=_('Topic'))
    content = models.TextField()

    class Meta:
        verbose_name = _("Forum Reply")
        verbose_name_plural = _("Forum Replies")
        ordering = ['-created']
        get_latest_by = 'created'

    def __unicode__(self):
        return self.content[:80]

class Topic(ForumTopic):
    """ A topic models which connect with reply sets. """
    subject = models.CharField(_('Topic Subject'), max_length=255, blank=False, null=False)
    r_num = models.PositiveIntegerField(default=0)
    v_num = models.PositiveIntegerField(default=0)
    closed = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    objects = ForumTopicManager()

    class Meta:
        ordering = ['-last_reply_on']
        get_latest_by = ('created_on')
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")

    def __unicode__(self):
        return self.subject

class Post(models.Model):
    """
    Posts is other threads of a topic.
    """
    topic = models.ForeignKey(Topic, verbose_name=_('Topic'))
    posted_by = models.ForeignKey(User)
    poster_ip = models.IPAddressField()
    topic_post = models.BooleanField(default=False)
    message = models.TextField()
    #attachments = models.ManyToManyField(Attachment, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null = True)
    edited_by = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ('-created_on',)
        get_latest_by = ('created_on', )

    def __unicode__(self):
        return self.message[:80]

    def subject(self):
        if self.topic_post:
            return _('Topic: %s') % self.topic.subject
        return _('Re: %s') % self.topic.subject

    """
    def update_attachments(self, attachment_ids):
        self.attachments.clear()
        for attachment_id in attachment_ids:
            try:
                attachment = Attachment.objects.get(pk=attachment_id)
            except:
                continue
            attachment.activated = True
            attachment.save()
            self.attachments.add(attachment)
    """

    @models.permalink
    def get_absolute_url(self):
        return (app_reverse('forum-post', 'feinx.apps.forum.urls', kwargs={'post_id': self.pk,}))

    def get_absolute_url_ext(self):
        topic = self.topic
        post_idx = topic.post_set.filter(created_on__lte=self.created_on). \
            count()
        page = (post_idx - 1) / DEFAULT_CTX_CONFIG['TOPIC_PAGE_SIZE'] + 1
        return '%s?page=%s#p%s' % (topic.get_absolute_url(), page, self.pk)

