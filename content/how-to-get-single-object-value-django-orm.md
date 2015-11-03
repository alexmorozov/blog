Title: Tip: How to get a single object`s value with Django ORM
Date: 2015-11-04 11:20
Category: Programming
Tags: django, python, orm

There are times when you want to get a single field of a single object in the
database. For example, just get the headline of the blog post #1, not fetching
it's body. How do you do it in a usual way?

    :::python
    >>> BlogPost.objects.only('headline').get(pk=1).headline
    'Hello world'

    # Or maybe even this way:
    >>> BlogPost.objects.values('headline').filter(pk=1)[0]['headline']
    'Hello world'

Recently I've stumbled upon [a shorter one](https://code.djangoproject.com/ticket/25132#comment:3):

    :::python
    >>> BlogPost.objects.values_list('headline', flat=True).get(pk=1)
    'Hello world'

As you can see, the trick is to chain `values()` and `get()` calls.
You may say "It's undocumented". Hah, face it, it [already is](https://docs.djangoproject.com/en/dev/ref/models/querysets/#values-list)! :)
