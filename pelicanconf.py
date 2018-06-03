#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Alex Morozov'
SITENAME = u'CTO with a CMO flavor'
SITEURL = 'https://morozov.ca'
SITELOGO = '/images/alex-morozov.jpg'

SITETITLE = SITENAME
SITESUBTITLE = "Alex Morozov's blog"

PATH = 'content'

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/category-%s.atom.xml'
TAG_FEED_ATOM = 'feeds/tag-%s.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

THEME = 'theme'
TYPOGRIFY = True

MARKDOWN = {
    'extensions': ['toc', 'codehilite', ],
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
    },
}


# Social widget
SOCIAL = (
    ('linkedin', 'https://linkedin.com/in/djangoengineer'),
    ('stack-overflow', 'http://stackoverflow.com/cv/django-developer'),
    ('twitter', 'https://twitter.com/alexmorozov'),
    ('github', 'https://github.com/alexmorozov'),
    ('facebook', 'https://facebook.com/theveryalexmorozov'),
    ('rss', '%s/%s' % (SITEURL, FEED_ALL_ATOM)),
)

LINKS = (
    #('About me', '#'),
    #('Hire me', '#'),
)

DISQUS_SITENAME = 'alexmorozovgithubio'
GOOGLE_ANALYTICS = 'UA-69605514-1'
GOOGLE_SITE_VERIFICATION = '51D-Oiso6ipK_s1K2_3GTokea7ou97KAqgICXkdRdFA'
ADD_THIS_ID = 'ra-563ca099f23dfb64'


DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
STATIC_PATHS = ['images', 'extra/CNAME', ]
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'}}

PLUGIN_PATHS = ['plugins', ]
PLUGINS = ['feed_summary', 'neighbors', 'summary', ]
FEED_USE_SUMMARY = True
SUMMARY_MAX_LENGTH = 80
