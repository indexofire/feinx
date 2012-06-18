# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.defaults import patterns, url
from feincms.models import Base
from feincms.content.application import models as app_models
from feincms.utils.managers import ActiveAwareContentManagerMixin


class ArticleManager(ActiveAwareContentManagerMixin, models.Manager):
    active_filters = {'simple-active': Q(active=True)}


class Article(Base):
    active = models.BooleanField(
        _('active'),
        default=True,
    )
    title = models.CharField(
        _('title'),
        max_length=255,
    )
    slug = models.SlugField(
        _('slug'),
        max_length=255,
        help_text=_('automatically generated from the title'),
        unique=True,
        editable=True,
    )

    class Meta:
        ordering = ['title']
        unique_together = []
        verbose_name = _('article')
        verbose_name_plural = _('articles')

    objects = ArticleManager()

    @classmethod
    def get_urlpatterns(cls):
        from .views import ArticleList, ArticleDetail
        return patterns('',
            url(r'^$', ArticleList.as_view(), name='article_index'),
            url(r'^(?P<slug>[a-z0-9_-]+)/$', ArticleDetail.as_view(), name='article_detail'),
        )

    @classmethod
    def remove_field(cls, f_name):
        """Remove a field. Effectively inverse of contribute_to_class"""
        # Removes the field form local fields list
        cls._meta.local_fields = [f for f in cls._meta.local_fields if f.name != f_name]

        # Removes the field setter if exists
        if hasattr(cls, f_name):
            delattr(cls, f_name)

    @classmethod
    def register_extension(cls, register_fn):
        """Extended from FeinCMS base to add the Admin class."""
        register_fn(cls, ArticleAdmin)

    @classmethod
    def get_urls(cls):
        return cls.get_urlpatterns()

    def __unicode__(self):
        return u"%s" % (self.title)

    @app_models.permalink
    def get_absolute_url(self):
        return ('article_detail', 'article.urls', (), {'slug': self.slug})

    @property
    def is_active(self):
        return Article.objects.active().filter(pk=self.pk).count() > 0
