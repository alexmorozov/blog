Title: How to send Jabber (XMPP) messages from Django
Date: 2015-11-11 12:20
Category: Programming
Tags: django, python, jabber, xmpp

![Django and Jabber]({filename}/images/jabber-logo.png)

<!-- PELICAN_BEGIN_SUMMARY -->
Did you ever want to have a simple Django notification bot? An intranet one
which just sends you (or someone you tell it to) Jabber messages when certain
events occur? So did I. Please, welcome: **[django-jabber][1]**.

<!-- PELICAN_END_SUMMARY -->

Installation and configuration are dead simple:

    :::shell
    pip install django-jabber

And then put this at your settings.py:

    :::python
    INSTALLED_APPS = (
        ...
        'django_jabber',
        ...
    )

    # Tweak settings below as necessary
    JABBER_HOST = 'jabber.domain.com'
    JABBER_USER = 'robot@domain.com'
    JABBER_PASSWORD = 'someStr0ngOne!1'
    JABBER_USE_TLS = True
    JABBER_USE_SSL = False
    JABBER_DRY_RUN = False  # Useful for testing

And we're done!

Now let's say you have an intranet forum. And you want to tell Bob and Alice
that new topic is posted:

    :::python
    from django_jabber import send_message

    recipients = ['bob', 'alice', ]
    topic = 'Hey there!'
    send_message(u'New topic: %s' % topic, recipients)

Notice we omit the `@domain` part in recipients' names. The package assumes you
use it in-house, having one domain. It would be easy, though, to make it
understand foreign domains (pull requests are welcome!).

That's it! Let me know if you have any ideas on improving this package.


[1]: https://github.com/alexmorozov/django-jabber
