Title: Managed search and replace in many files using Vim and ag.
Date: 2015-11-16 10:20
Category: Programming
Tags: vim, ag

Recently I faced an interesting problem. I had to search for the [redundant
lines of code][1] (about a hundred occurences), and replace **some** of them.
The bad thing is that I _couldn't do that automatically_, as each case had to
be manually reviewed.

So, how to automate this task, while keeping the manual control?

<!-- PELICAN_END_SUMMARY -->

The text what I was looking for were actually two consecutive lines:

    :::python
        self.assertEqual(response.status_code, ...)
        self.assertContains(response, ...)

Let's fire up the [ag][2] utility (a faster and feature-full fgrep
replacement):

    :::bash
        user@host:~/src$ ag 'self.assertEqual\(response.status.{0,100}\s*self.assertContains' . | vi -

The trick here is that ag uses multiline matching by default, therefore
allowing us to search for several lines at once. And we pipe the search results
to Vim, my editor of choice.

Now we have a Vim window with a bunch of lines like:

    ...
    tests/test_client/tests.py:732:        self.assertEqual(response.status_code, 200)
    tests/test_client/tests.py:733:        self.assertContains(response, 'This is a test')
    tests/test_client/tests.py:743:        self.assertEqual(response.status_code, 200)
    tests/test_client/tests.py:744:        self.assertContains(response, echoed_request_line)
    tests/admin_views/tests.py:230:        self.assertEqual(response.status_code, 200)
    tests/admin_views/tests.py:231:        self.assertContains(response, 'value="My Section"',
    ...

, and we definitely need a way to easily navigate to each file (preferably in
the split window), analyze the case and make changes.

Vim superpowers to the rescue! Let's make a convenient shortcut:

    :nnoremap <CR> :vertical wincmd F<CR>

Simply put, we create a new mapping for the Vim's normal (navigation) mode.
When we hit `Enter` (or `<CR>`), Vim makes a vertical split and executes the
window command `F`, which is essentially to open a file under cursor and
navigate to the specified line.

So we basically scroll down the search results, hit `Enter` on interesting
ones, and have them opened for editing in a split window. Cool? You bet.

Do you have some Vim find-n-replace tips? Share them in comments!

[1]: https://code.djangoproject.com/ticket/25780
[2]: https://github.com/ggreer/the_silver_searcher
