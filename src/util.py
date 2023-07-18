# _() is a function that does literally nothing, but we need to wrap our
# translatable strings in it so that gettext can figure out what needs
# translating, and build those translation strings for us.
_ = lambda x: x
