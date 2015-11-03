Title: When you shouldn't use the Django admin
Date: 2015-11-03 10:20
Category: Programming
Tags: django, python, admin


In case you've thought I detest `django.contrib.admin` -- by no means.
Actually it's one of the Django's greatest features, I really love it. In most
cases.

Here's a real life story. We've had to quickly put up the first version of an
intranet claim tracking system, and one of our developers was just crazy about
the Django admin... So why not, we've got along with the stock interface as the
primary one for our users.

3 years after that, I know for sure: I'm the person who knows all the drawbacks
of such decision. And I want to share them with you.

Here's my top 6 list of problems:

### Stock templates updates

The worst thing is often they pass through the testing sieve. Tests pass,
layout is broken, users complain. Upcoming 1.9 version introduces new flat
design and I'm just afraid to upgrade.

### Unstable javascript API

Unlike the regular Django APIs, javascript ones are not guaranteed to be
stable. In addition, they are not so customizable - for example, you just can't
set a popup width without overriding the whole file.  On the other hand,
namespaced jQuery is really good. Most probably you won't have any versioning
problems between upgrades if you use additional jQuery for your own purposes.

### Insufficient default permissions

If you want to see a list of objects, Django admin gives you a convenient
'changelist' view. You can tweak in a lot of ways, which is cool, but there's a
major problem: to see a changelist, one has to have the 'change' permission.
While it's perfectly normal for basic sites, more complex setups often need the
'view' permission, which allows to view a list of, say, tickets, while not
allowing to edit them.

So one have to decide: whether to lose the changelist functionality, or to
override the changelist view by copy-pasting 90% of the code. Bad decisions, I
must say.

### No chance of using generic CBVs

I imagine some day we will see the Django admin based on the generic
class-based views. For now, if other parts of your site use CBVs for shared
behaviour, you must have some additional glue to add this behaviour to the
admin. You may recall context processors and middleware, but in my opinion
they are not as handy as a class tree.

### Monolythic implementation

The `django.contrib.admin.options` module is about 1 900 lines. I must say
the most of that code is very readable and straightforward, but dude, almost 2K
lines in one file! Reminds me of that Flask one-file web apps - you know, 10K
lines is not the limit. For those who interested, only `django.db.models`
package have some larger files.

### Fieldsets handle only the basic cases

As for the admin fieldsets, they're very handy when you work with relatively
simple models. If you want to organize some kind of tabs, collapsible
fieldsets, etc - you will have to code your own or to use custom modules.

## So what?

To make sure you get me right: the above is not about how bad the Django admin
is. It's about not putting too much expectations on the rather simple tool. So
dont repeat our mistakes. For me, here's the formula:

Consider to stick with Django admin if two conditions are met:

* You expose the admin to the small group of experienced users (content managers)
* Your models, relations and workflow are simple enough.
