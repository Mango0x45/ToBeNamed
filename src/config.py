from enum import StrEnum

AVAILABLE_LOCALES = {"en_GB", "en_US"}


class Cookie(StrEnum):
	REDIRECT = "redirect"
	LOCALE = "locale"
