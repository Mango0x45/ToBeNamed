import enum
from datetime import datetime
from enum import Enum, EnumMeta, StrEnum
from typing import Any, LiteralString, NamedTuple, Self

from util import _


class EnumContains(EnumMeta):
	def __contains__(cls, other: Any) -> bool:
		try:
			cls(other)
		except ValueError:
			return False
		return True


class Cookie(StrEnum):
	LOCALE = "locale"
	REDIRECT = "redirect"
	THEME = "theme"


class Theme(StrEnum):
	DARK = "dark"
	LIGHT = "light"


# We use strings instead of floats because the frontend is going to send us
# strings in our request arguments anyways.  The flask_babel.format_XXX() methods
# also work with strings in all places where they’d want a number.
DENOMINATIONS = ("0.01", "0.02", "0.05", "0.10", "0.20", "0.50", "1.00", "2.00")


class Locale(StrEnum, metaclass=EnumContains):
	# Eurozone
	EN_GB = "en_GB"

	# International
	EN_US = "en_US"

	def as_html_lang(self) -> str:
		return self.replace("_", "-")


class Country(NamedTuple):
	iso_3166_1: str
	name: str

	def __eq__(self, other: object) -> bool:
		match other:
			case str():
				return self.iso_3166_1.casefold() == other.casefold()
			case Country():
				return self.iso_3166_1.casefold() == other.iso_3166_1.casefold()
			case _:
				return False

	# We want to use ISO 3166-1 Alpha-2 codes everywhere unless explicitly stated
	# otherwise.
	def __str__(self) -> str:
		return self.iso_3166_1


COUNTRIES = (
	Country("ad", _("Andorra")),
	Country("de", _("Germany")),
)
