Title: When you SHOULD use the Django admin: 9 tips
Date: 2015-11-16 10:20
Category: Programming
Status: draft
Tags: django, python, admin

This post is inspired by a comment on Reddit concerning my [recent post][1]:

> "The problem is that everyone I speak to seems to think the opposite - that
> the admin is super-limited, inflexible and hard to customize."
>
> -- <cite>[andybak][2]</cite>

I'm willing to beat this prejudice right now. The Django admin is a really
brilliant piece of software, which can significantly speed up your development.

Here are some tips about the Django admin, which I've found to be quite useful.

### TIP #1: The Django admin is not just for Django sites.

While the admin interface plays very well with the rest of Django framework,
it's very easy to use it with, say, the legacy database or the site which has
an awkward admin interface. And quite often it's the best way of testing if
Django will suit your needs.

You just have to:

1. Create a new application in your Django project and make sure you've
   configured the connection to the legacy DB in your `DATABASES` setting.
1. Define your data tables as Django models. A pretty useful `manage.py
   inspectdb` command does exactly what its name implies: inpects the existing
   database and prints out the auto-generated Django models.
2. Create an `admin.py` file and put there, er, the admin stuff. More on this
   in a moment.

So let's imagine we have a simple site where visitors post pictures of cute
animals and leave comments on them. The site is written in Brainf\*ck, so the
admin interface looks like... You know, not that good.

To remedy it, we resembled the database structure with several Django models
and put toghether a simple admin interface:

    :::python
    # models.py
    class Picture(models.Model):
        DOG = 1
        CAT = 2
        ANIMAL_KIND_CHOICES = (
            (DOG, 'dog'),
            (CAT, 'cat'),
        )

        title = models.CharField(max_length=200)
        author = models.ForeignKey(Author, related_name='comments')
        animal_kind = models.IntegerField(choices=ANIMAL_KIND_CHOICES)
        photo = models.ImageField(upload_to='animals')
        is_promoted = models.BooleanField(default=False)


    class Author(models.Model):
        name = models.CharField(max_length=100)
        email = models.EmailField()


    class Comment(models.Model):
        author = models.ForeignKey(Author, related_name='comments')
        picture = models.ForeignKey(Picture, related_name='comments')
        comment = models.TextField()
        editors_note = models.TextField()

    # admin.py
    class PictureAdmin(admin.ModelAdmin):
        list_display_fields = ('photo', 'animal_kind', 'author', 'is_promoted', )


    class AuthorAdmin(admin.ModelAdmin):
        list_display_fields = ('name', 'email', )


    class CommentAdmin(admin.ModelAdmin):
        list_display_fields = ('picture', 'author', )


### Search on multiple fields and relations

Okay, let's talk about the search. The default admin search box is quite
useful, but is somewhat limited. We want it to search in pictures' titles,
authors' names and comments' texts. How to achieve that?

    :::python
    class PictureAdmin(admin.ModelAdmin):
        search_fields = ('title', 'author__name', 'comments__text', )

Apparently, there are too many users to list them as a filter at sidebar.

### Filter your data the way you like

A lot of people use the ModelAdmin's ability to filter on specific fields. You
know, put a field name to the `list_filter` attribute and here we go. But it's
also extremely easy to create a custom filters!

One day you decide to send a "thank you" email to all authors who have 100+
posts. How do we distinguish them? Let's create a filter and add it to the our
changelist.

    :::python
    class ProductiveAuthorsFilter(admin.SimpleListFilter):
        parameter_name = 'is_productive'
        title = 'Productive author'
        YES, NO = 1, 0

        # Number of comments for an author to be considered a productive one
        THRESHOLD = 100

        def lookups(self, request, model_admin):
            return (
                (self.YES, 'yes'),
                (self.NO, 'no'),
            )

        def queryset(self, request, queryset):
            qs = queryset.annotate(Count('comments'))

            # Note the syntax. This way we avoid touching the queryset if our
            # filter is not used at all.

            if self.value() == self.YES:
                return qs.filter(comments__count__gte=self.THRESHOLD)
            if self.value() == self.NO:
                return qs.filter(comments__count__lt=self.THRESHOLD)

            return queryset


    class PictureAdmin(admin.ModelAdmin):
        list_filters = [..., ProductiveAuthorsFilter]

Now we can easily select our core authors. So how to send them an email? Let's
move on to the next section.

### TIP FIXME: Add common actions to the admin

We have an 'actions' toolbox on our changelist. It is very handy if we could
select some pictures and make them as "promoted" with a single click. Let's
implement it:

    :::python
    class PictureAdmin(admin.ModelAdmin):
        actions = ['promote', ]

        def promote(self, request, queryset):
            queryset.update(is_promoted=True)
            self.message_user('The posts are promoted')
        promote.short_description = 'Promote the pictures'

And that's it! If fact, it's quite easy to extend our action further, adding,
for example, an interdemiate form. Django docs
have an [excellent section][3] on this.


### TIP FIXME: Open an object's page – an easy way

A very common need is to open the object's public page on site. By default you
have to open the object's form and then click on the `View on site` button.
That's how to ease it a bit:

    :::python
    class PictureAdmin(admin.ModelAdmin):
        list_fields = [..., 'object_link']

        def object_link(self, item):
            url = item.get_absolute_url()
            return u'<a href={url}>open</a>'.format(url=url)
        object_link.short_description = 'Open on site'
        object_link.allow_tags = True

You'll probably want to move this piece of code to a mixin, or to a shared base
admin class.


custom actions (incl. dynamic)
custom links/buttons
list_select_related instead of overriding get_queryset
true readonly admin
    your grandma wants to see a list, but you're afraid she will ruin a whole
    site if there is a single button.
ordering
    order comments?
custom view (get_urls)
    send a email
list_display_links
list_editable
show totals
some tips about forms? Fieldsets?

somefield__afieldsmethod
### Override another module's admin


bonus tip

leave a comment in reddit thread when done, cross-link both articles.

[1]: {filename}/when-you-shouldnt-use-django-admin.md
[2]: https://www.reddit.com/r/django/comments/3sfg0x/when_you_shouldnt_use_the_django_admin/
[3]: https://docs.djangoproject.com/en/1.8/ref/contrib/admin/actions/#actions-that-provide-intermediate-pages
