#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Alex Morozov'
SITENAME = u'CTO with a CEO flavour'
SITEURL = 'https://alexmorozov.github.io'
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


# Social widget
SOCIAL = (
    ('linkedin', 'https://linkedin.com/in/djangoengineer'),
    ('github', 'https://github.com/alexmorozov'),
    ('rss', '%s/%s' % (SITEURL, FEED_ALL_ATOM)),
)

LINKS = (
    #('About me', '#'),
    #('Hire me', '#'),
)

DISQUS_SITENAME = 'alexmorozovgithubio'
GOOGLE_ANALYTICS = 'UA-69605514-1'
ADD_THIS_ID = 'ra-563ca099f23dfb64'


DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
STATIC_PATHS = ['images', ]

PLUGIN_PATHS = ['plugins', ]
PLUGINS = ['feed_summary', 'neighbors', ]
FEED_USE_SUMMARY = True
SUMMARY_MAX_LENGTH = 80
