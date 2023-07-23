from enum import StrEnum

AVAILABLE_LOCALES = {"en_GB", "en_US"}


class StrEnumContains(StrEnum):
	@classmethod
	def __contains__(cls, key: str) -> bool:
		return key in cls.__members__.values()


class Cookie(StrEnum):
	LOCALE = "locale"
	REDIRECT = "redirect"
	THEME = "theme"


class Theme(StrEnum):
	DARK = "dark"
	LIGHT = "light"
