from typing import TypeVar

T = TypeVar("T")

# _() is a function that does literally nothing, but we need to wrap our
# translatable strings in it so that gettext can figure out what needs
# translating, and build those translation strings for us.
def _(x: T) -> T:
	return x
