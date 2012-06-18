# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import get_callable
from feincms.admin.item_editor import ItemEditor
from .models import Article


ModelAdmin = get_callable(getattr(settings, 'ARTICLE_MODELADMIN_CLASS', 'django.contrib.admin.ModelAdmin'))

class ArticleAdmin(ItemEditor, ModelAdmin):
    list_display = ['__unicode__', 'active',]
    list_filter = []
    search_fields = ['title', 'slug']
    filter_horizontal = []
    prepopulated_fields = {
        'slug': ('title',),
    }
    fieldsets = [
        (None, {
            'fields': ['active', 'title', 'slug']
        }),
    ]


admin.site.register(Article, ArticleAdmin)
