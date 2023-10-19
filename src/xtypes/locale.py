from typing import Self

from xtypes.case_insensitive_string import CaseInsensitiveString


class Locale:
	__slots__ = ("iso_639_1", "iso_3166_1", "name", "enabled")

	def __init__(
		self, iso_639_1: str, iso_3166_1: str, name: str, enabled: bool
	) -> None:
		self.iso_639_1 = CaseInsensitiveString(iso_639_1)
		self.iso_3166_1 = CaseInsensitiveString(iso_3166_1)
		self.name = name
		self.enabled = enabled

	def __eq__(self, other: object) -> bool:
		match other:
			case Locale():
				return (
					self.iso_639_1 == other.iso_639_1
					and self.iso_3166_1 == other.iso_3166_1
				)
			case str():
				return str(self).casefold() == other.casefold()
			case _:
				return False

	def __str__(self) -> str:
		return f"%s_%s" % (self.iso_639_1.lower(), self.iso_3166_1.upper())

	def as_lang(self) -> str:
		return f"%s-%s" % (self.iso_639_1.lower(), self.iso_3166_1.upper())

	@classmethod
	def from_str(cls, locale: str) -> Self:
		i = LOCALES.index(locale)
		return LOCALES[i if i != -1 else LOCALES.index("en_GB")]


EZ_LOCALES = (
	Locale("ca", "AD", "català", False),
	Locale("de", "DE", "Deutsch", False),
	Locale("el", "GR", "ελληνικά", False),
	Locale("en", "GB", "English", True),
	Locale("es", "ES", "español", False),
	Locale("et", "EE", "eesti", False),
	Locale("fi", "FI", "suomi", False),
	Locale("fr", "FR", "français", False),
	Locale("ga", "IE", "Gaeilge", False),
	Locale("hr", "HR", "hrvatski", False),
	Locale("it", "IT", "italiano", False),
	Locale("lt", "LT", "lietuvių", False),
	Locale("lv", "LV", "latviešu", False),
	Locale("mt", "MT", "Malti", False),
	Locale("nl", "NL", "Nederlands", True),
	Locale("pt", "PT", "português", False),
	Locale("sk", "SK", "slovenčina", False),
	Locale("sl", "SI", "slovenščina", False),
)

WORLD_LOCALES = (
	Locale("bg", "BG", "български", False),
	Locale("en", "US", "English\x0A(US)", True),
	Locale("ro", "RO", "română", False),
)

LOCALES = EZ_LOCALES + WORLD_LOCALES
