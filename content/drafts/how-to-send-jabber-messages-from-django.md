Title: How to send Jabber(XMPP) messages from Django
Date: 2015-11-10 10:20
Category: Programming
Tags: django, python, jabber, xmpp


Ever wanted to have a simple Django notification bot? A one which just sends
you Jabber messages when certain events occur? Please, welcome: [django-jabber][1].

Installation and configuration are dead simple:

    :::shell
    pip install django-jabber

    :::python
    # Put this at your settings.py
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

Now let's say you want to inform some users about the 

    :::python
    from django_jabber import send_message

    recipients = ['bob', 'alice', ]
    send_message(u'Hello there', recipients)

Notice we omit the `@domain` part in users names, since they are the same for all users within the domain.

We use it in intranet solutions, so far so good.


[1]: (https://github.com/alexmorozov/django-jabber)
