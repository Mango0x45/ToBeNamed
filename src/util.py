import copy
import os.path
from typing import Callable, Iterable, TypeVar

import flask_babel
from icu import Collator, InvalidArgsError
from icu import Locale as IcuLocale

T = TypeVar("T")


def locale_sort(
	xs: Iterable[T], key: Callable[[T], str] = lambda x: str(x)
) -> Iterable[T]:
	"""
	Return a sorted copy of ‘xs’ that takes into account the current locale.
	You may also specify a ‘key’ function that works identically to the key
	function that may be provided to the standard python ‘sorted()’ function.

	In the case that the current locale cannot be determined, a copy of the
	original array is returned.
	"""
	try:
		locale = IcuLocale(str(flask_babel.get_locale()))
	except InvalidArgsError:
		return copy.copy(xs)
	else:
		collator = Collator.createInstance(locale)
		return sorted(xs, key=lambda x: collator.getSortKey(key(x)))


def strip_jinja(s: str) -> str:
	"""
	Strip Jinja tags (‘{{’ & ‘}}’) and the translation function (‘_()’) from the
	given string.
	"""
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


def from_root(s: str) -> str:
	"""
	Get a file path for the file ‘s’ relative to the root of the ‘src/’
	directory.
	"""
	return os.path.join(os.path.dirname(__file__), s)
