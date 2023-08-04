from typing import TypeVar

T = TypeVar("T")


def _(x: T) -> T:
	"""
	_() is a function that does literally nothing, but we need to wrap our
	translatable strings in it so that gettext can figure out what needs
	translating, and build those translation strings for us.
	"""
	return x


def strip_jinja(s: str) -> str:
	s = s.strip().removeprefix("{{").removesuffix("}}").strip()
	if s.startswith("_("):
		s = (
			s.removeprefix("_(")
			.removesuffix(")")
			.strip()
			.removeprefix('"')
			.removesuffix('"')
		)
	return s
