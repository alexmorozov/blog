Title: Why you should use the Django admin: 9 tips
Date: 2015-12-9 10:20
Category: Programming
Tags: django, python, admin

![Django admin is, you know, magic]({filename}/images/django-pony.png)

<!-- PELICAN_BEGIN_SUMMARY -->

This writing is inspired by a comment on Reddit concerning my [recent post][1]:

> "The problem is that everyone I speak to seems to think the opposite - that
> the admin is super-limited, inflexible and hard to customize."
>
> -- <cite>[andybak][2] on Reddit</cite>

I'm about to break this prejudice right now. The Django admin is a really
brilliant piece of software, which can significantly speed up your development.

Here are some tips about the Django admin, which I've found to be quite useful.

<!-- PELICAN_END_SUMMARY -->

<small>
(A bit of terminology for those of us who isn't that familiar with the Django admin)

> **Changeform** is the page where you can edit the object.
>
> **Changelist** is the page which lists all objects of specific kind. You can filter and execute actions on the subset of objects. Clicking on the object in the changelist usually gets you to that object's changeform.
</small>

To make the tips more practical, let's try to solve some almost-real-life
problems. So say we have a simple site where visitors post pictures of cute
animals and leave comments on them. Should be quite popular, shouldn't it?

### Tip #1: The Django admin is not just for Django sites

While the admin interface plays very well with the rest of Django framework,
it's very easy to use it with, say, the legacy database or the site which has
an awkward admin interface. And quite often it's the best way of testing if
Django will suit your needs.

All you need is to:

1. Create a new application in your Django project and make sure you've
   configured the connection to the legacy DB in your `DATABASES` setting.
1. Define your data tables as Django models. A pretty useful `manage.py
   inspectdb` command does exactly what its name implies: inpects the existing
   database and prints out the auto-generated Django models.
2. Create an `admin.py` file and put there, er, the admin stuff. More on this
   in a moment.

Speaking of our animals' site, it is written in [Brainf\*ck][5], so the admin
interface looks like... You know, not that good.  To fix it, we resembled
the database structure with several Django models and put together a simple
admin interface:

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
        author = models.ForeignKey(Author, related_name='pictures')
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


### Tip #2: Filter your data the way you like

A lot of people use the Django admin's ability to filter on specific fields.
You know, put a field name to the `list_filter` attribute and here we go. But it's
also extremely easy to create a custom filters!

Suppose eventually you decide to promote all the authors having 100+ posts.
But how do we distinguish them? Let's create a filter and add it to the our
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

Now we can easily select our core authors. How do we actually promote them then?
Let's move on to the next section.

### Tip #3: Put the common stuff to 'actions'

This one is a true godsend for content managers. Remember the 'actions' toolbox
at the top of each model's list? It would be very handy if we select some
pictures and make them "promoted" with a single click, right? Let's
implement it:

    :::python
    class PictureAdmin(admin.ModelAdmin):
        actions = ['promote', ]

        def promote(self, request, queryset):
            queryset.update(is_promoted=True)
            self.message_user(request, 'The posts are promoted')
        promote.short_description = 'Promote the pictures'

And that's it! No longer opening each form one by one! Plus, it's quite easy
to extend our action further, adding, for example, an intermediate form. Django
docs have an [excellent section][3] on this.

### Tip #4: Search on all fields you need

Okay, filters are cool but let's focus a bit on the search facility. In almost all
installations I've seen the search box is used for searching across one model's
fields. But the Django search really shines when you realize it can handle the
relationships. So assume we want it to search in pictures' titles, authors'
names and comments' texts. How do we achieve that?

    :::python
    class PictureAdmin(admin.ModelAdmin):
        search_fields = ('title', 'author__name', 'comments__text', )

Just don't forget to add some full-text indices, if your database is big enough.

### Tip #5: View an object's page – an easy way

A very common need is to view the object's public page on site. By default you
have to browse to the object's form and then click on the "View on site" button.
That's how to make it a bit easier:

    :::python
    class PictureAdmin(admin.ModelAdmin):
        list_fields = [..., 'object_link']

        def object_link(self, item):
            url = item.get_absolute_url()
            return format_html(u'<a href="{url}">open</a>', url=url)
        object_link.short_description = 'View on site'

This snippet adds a "View on site" link to each object in the list. Here we
assume you've already implemented the `get_absolute_url()` method on your
model. If not - go ahead and do it, it'll save you much time. And you'll
probably want to move this snippet to a mixin, or a shared base admin class.

### Tip #6: Edit fields in-place right on the list page

Suppose we need to put an editor's note to each comment. And naturally enough,
we don't want to open each comment's changeform. To implement this, adjust your ModelAdmin a bit:

    :::python
    class CommentAdmin(admin.ModelAdmin):
        list_display_fields = ('picture', 'author', 'editors_note', )
        list_editable = ('editors_note', )

That's literally all. Now you can open a comments list, filter it down
to your needs, and start writing notes away.

### Tip #7: Customize your totals with the data you really need

There's a totals line at the bottom of each changelist. Imagine we'd like to
separate the counts of dogs' and cats' pics. This functionality will take a bit
more of code: we have to override the changelist itself, as well as the html
template (more on [template overriding][4]).

    :::python
    from django.contrib.admin.views.main import ChangeList

    class PicturesChangeList(admin.ChangeList):
        def get_results(self, request):
            super(PicturesChangeList, self).get_results(request)
            totals = self.result_list.aggregate(
                dogs_count=Sum(Case(When(animal_kind=Picture.DOG, then=1),
                               output_field=IntegerField())),
                cats_count=Sum(Case(When(animal_kind=Picture.CAT, then=1),
                               output_field=IntegerField())))
            self.totals = totals


    class PictureAdmin(admin.ModelAdmin):
        def get_changelist(self, request):
            return PicturesChangeList

and the template:

    :::html
    {% extends 'admin/change_list.html' %}
    {% block result_list %}
        {{ block.super }}
        <p>
            There are
            <strong>
                {{ cl.totals.dogs_count|default:'none' }} dogs and
                {{ cl.totals.cats_count|default:'none' }} cats
            </strong>
            on this page.
        </p>
    {% endblock %}

### Tip #8: Readonly admin interface for some of us

Guess what? Your grandma wants to take a look at all these cuties, and she
loves the Django admin interface she watched over your shoulder. But you're sure she
will ruin the whole site if there is a single button. Okay, let's put together
the grandma-proof&trade; readonly admin interface (who's said "databrowse"?):

    :::python
    class GrandmaProofAdmin(admin.ModelAdmin):
        def get_readonly_fields(self, request, obj=None):
            if request.user.username == 'granny':
                return [f.name for f in self.model._meta.fields]
            else:
                return super(GrandmaProofAdmin, self).get_readonly_fields(request, obj)


    class PictureAdmin(GrandmaProofAdmin):
        ...

Now you can safely grant your granny the `change pictures` permission in order
to see the pictures list. Note that this solution surely will not suit any
serious usage - you'll need to handle [some more cases][6].


### Tip #9: Per-object custom actions

Sometimes you want to execute a certain action on only one object. The
'actions' toolbox surely makes it possible, but ticking the object, selecting
the action, clicking on a button... There should be a more convenient way,
shouldn't it? Let's reduce all that stuff to actually clicking on a button.

This time we will be implementing another granny's big idea. She'd like to send
an email to some authors, showing all her love.

    :::python
    class PictureAdmin(admin.ModelAdmin):
        list_fields = (..., 'mail_link', )

        def mail_link(self, obj):
            dest = reverse('admin:myapp_pictures_mail_author',
                           kwargs={'pk': obj.pk})
            return format_html('<a href="{url}">{title}</a>',
                               url=dest, title='send mail')
        mail_link.short_description = 'Show some love'
        mail_link.allow_tags = True

        def get_urls(self):
            urls = [
                url('^(?P<pk>\d+)/sendaletter/?$',
                    self.admin_site.admin_view(self.mail_view),
                    name='myapp_pictures_mail_author'),
            ]
            return urls + super(PictureAdmin, self).get_urls()

        def mail_view(self, request, *args, **kwargs):
            obj = get_object_or_404(Picture, pk=kwargs['pk'])
            send_mail('Feel the granny\'s love', 'Hey, she loves your pet!',
                      'granny@yoursite.com', [obj.author.email])
            self.message_user(request, 'The letter is on its way')
            return redirect(reverse('admin:myapp_picture_changelist'))

Hope now she's happy. A link has appeared along each object's fields, allowing
her to send a mail by simply clicking it.

### Bonus Tip: Reduce queries by adding a single line to your admin

The most common tip about the Django admin (and Django in general) is
(worthily) the `select_related` stuff. Ok, ok, you all know it. Preload the
related objects by passing their names to the `list_select_related` ModelAdmin
attribute.  But did you know you haven't to specify all your relations? Just
set it to `True`, and Django will automatically preload foreign objects:

    :::python
    class PictureAdmin(admin.ModelAdmin):
        list_select_related = True

So guys, that's it, hope you've liked it. Got any cool tips? Go ahead and share
your favorite ones in comments!

[1]: {filename}/when-you-shouldnt-use-django-admin.md
[2]: https://www.reddit.com/r/django/comments/3sfg0x/when_you_shouldnt_use_the_django_admin/
[3]: https://docs.djangoproject.com/en/1.8/ref/contrib/admin/actions/#actions-that-provide-intermediate-pages
[4]: https://docs.djangoproject.com/en/1.9/ref/contrib/admin/#overriding-admin-templates
[5]: https://en.wikipedia.org/wiki/Brainfuck
[6]: https://gist.github.com/aaugustin/1388243


<!---


custom actions (incl. dynamic)
custom links/buttons
ordering
    order comments?
list_display_links
some tips about forms? Fieldsets?
somefield__afieldsmethod
Override another module's admin

--------------------------------------------

leave a comment in reddit thread when done

--->

