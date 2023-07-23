from enum import EnumMeta, StrEnum
from typing import Any


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


class Locale(StrEnum, metaclass=EnumContains):
	# Eurozone
	EN_GB = "en_GB"

	# International
	EN_US = "en_US"

	def as_html_lang(self) -> str:
		return self.replace("_", "-")
