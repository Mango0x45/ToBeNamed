# Making a Contribution


## Commits

Commit messages should be short and to the point.  They should begin with a
capital letter and use proper English casing, and should not be in the past
tense.  An example of a good commit message is ‘Add Catalan translations’.  An
example of a bad commit message is ‘added catalan translations for the coin
designs page’.

If you have additional information about your changes you’d like to detail, such
as the specific scope of your changes, please make use of the commit
description.

Commits themselves should also be small and easy to follow.  If one large
contribution requires 5 different steps, make 5 different commits, not one giant
one.


## Formatting

When working with Python code, do not forget to run `make format` before you
commit to ensure your work is properly formatted.  When working with Jinja, CSS,
etc. there is no specific formatting standard but just try to stick to the same
style as the rest of the project.


### Jinja Translations

Just a clarification about Jinja code-style when working with translations.  If
your translatable string is short and fits on one line, use the `_()` function:

    <p>{{ _("Hi how are you?") }}</p>

If the string is long or spans over multiple lines, you should instead use the
`{% trans %}` syntax:

    <p>
        {% trans %}
        This is a much longer string that spans over multiple lines.  It is
        important here to use the trans-block to ensure this gets extracted
        properly!
        {% endtrans %}
    </p>
