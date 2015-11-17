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
But before we start, let's imagine we have a simple site where visitors post
pictures of cute animals and leave comments on them.

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


    class Author(models.Model):
        name = models.CharField(max_length=100)
        email = models.EmailField()


    class Comment(models.Model):
        author = models.ForeignKey(Author, related_name='comments')
        picture = models.ForeignKey(Picture, related_name='comments')
        comment = models.TextField()
        is_promoted = models.BooleanField(default=False)
        editors_note = models.TextField()

    # admin.py
    class PictureAdmin(admin.ModelAdmin):
        list_display_fields = ('photo', 'animal_kind', )


    class CommentAdmin(admin.ModelAdmin):
        pass


### Override another module's admin

### Search on multiple fields and relations

The default admin search box is quite useful, but is somewhat limited. We want it
to search in pictures' titles, authors' names and comments' texts. How to
achieve that?

    :::python
    class PictureAdmin(admin.ModelAdmin):
        search_fields = ('title', 'author__name', 'comments__text', )


Apparently, there are too many users to list them as a filter at sidebar.

custom list filters
    having more than 100 comments
custom actions (incl. dynamic)
    mark as editors_pick
object on site link
    get_absolute_url
custom links/buttons
list_select_related instead of overriding get_queryset
true readonly admin
    your grandma wants to see a list, but you're afraid she will ruin a whole
    site if there will be a single button.
ordering
    order comments?
custom view (get_urls)
    send a email
list_display_links
list_editable
show totals
some tips about forms? Fieldsets?

bonus tip

leave a comment in reddit thread when done, cross-link both articles.

[1]: {filename}/when-you-shouldnt-use-django-admin.md
[2]: https://www.reddit.com/r/django/comments/3sfg0x/when_you_shouldnt_use_the_django_admin/
