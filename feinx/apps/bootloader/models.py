# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.application.models import ApplicationContent
from feincms.content.richtext.models import RichTextContent
from feincms.content.image.models import ImageContent
from feincms.content.comments.models import CommentsContent
from feincms.content.medialibrary.v2 import MediaFileContent
from feincms.content.raw.models import RawContent

#from feinx.content.markup.models import MarkupContent
#from feinx.content.form.models import FormContent
#from feinx.content.googlemap.models import GoogleMapsContent
#from feinx.content.gallery.models import GalleryContent

# Register page extensions
Page.register_extensions(
    'datepublisher',
    'translations',
    'changedate',
    'navigation',
    'seo',
    'symlinks',
    'titles',
    #'feincms_extension.page.auth',
)

# Register Templates used in pages
Page.register_templates(
    {
        'key': 'index',
        'title': _('Index Page'),
        'path': 'site_index.html',
        'regions': (
            ('main', _('Main content area')),
        ),
    },
    {
        'key': 'col_1',
        'title': _('One Columns Page'),
        'path': 'site_col_one.html',
        'regions': (
            ('main', _('Main content area')),
        ),
    },
    {
        'key': 'col_2',
        'title': _('Two Columns Page'),
        'path': 'site_col_two.html',
        'regions': (
            ('main', _('Main content area')),
            ('left', _('Left Side'), 'inherited'),
        ),
    },
    {
        'key': 'col_3',
        'title': _('Three Columns Page'),
        'path': 'site_col_three.html',
        'regions': (
            ('main', _('Main content area')),
            ('sidebar', _('Sidebar'), 'inherited'),
            ('right', _('Right Side'), 'inherited'),
        ),
    },
    {
        'key': 'under_construction',
        'title': _('Under Construction'),
        'path': 'under_construction.html',
        'regions': (
            ('main', _('Main content area')),
        ),
    },
    {
        'key': 'lab_member',
        'title': _('Lab Member'),
        'path': 'isotope.html',
        'regions': (
            ('main', _('Main content area')),
            ('left', _('Left Side'), 'inherited'),
        ),
    },
    {
        'key': 'examples',
        'title': _('Examples'),
        'path': 'examples.html',
        'regions': (
            ('main', _('Main content area')),
            ('left', _('Left Side'), 'inherited'),
        ),
    },
)


# Add rich content type
Page.create_content_type(RichTextContent)

# Add image content type
Page.create_content_type(
    ImageContent,
    POSITION_CHOICES=(
        ('block', _('block')),
        ('left', _('left')),
        ('right', _('right')),
    )
)

# Add markup content type
#Page.create_content_type(MarkupContent)

# Add google maps content type
#Page.create_content_type(GoogleMapsContent)

# Add table content type
#Page.create_content_type(TableContent)

# Add applications in pages
Page.create_content_type(
    ApplicationContent,
    APPLICATIONS=(
        ('feinx.apps.forum.urls', _('Forum Application')),
        ('feinx.contrib.account.urls', _('Account Application')),
        #('news.urls', _('News Application')),
        #('article.urls', _('Library Application')),
        #('document.urls', _('Document Application')),
    )
)

# Add form content type
#Page.create_content_type(FormContent)

# Add comment content type
Page.create_content_type(CommentsContent)

# Add Media Library
Page.create_content_type(
    MediaFileContent,
    TYPE_CHOICES=(
        ('lightbox', _('lightbox')),
        ('download', _('download')),
    )
)

# Add raw content type
Page.create_content_type(RawContent)

# Create reversion
#Page.register_with_reversion()

# Add gallery content type
#Page.create_content_type(GalleryContent)
