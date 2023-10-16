from typing import Self

from xtypes.case_insensitive_string import CaseInsensitiveString


class Locale:
	__slots__ = ("iso_639_1", "iso_3166_1", "name")

	def __init__(self, iso_639_1: str, iso_3166_1: str, name: str) -> None:
		self.iso_639_1 = CaseInsensitiveString(iso_639_1)
		self.iso_3166_1 = CaseInsensitiveString(iso_3166_1)
		self.name = name

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
	Locale("ca", "AD", "català"),
	Locale("de", "DE", "Deutsch"),
	Locale("el", "GR", "ελληνικά"),
	Locale("en", "GB", "English"),
	Locale("es", "ES", "español"),
	Locale("et", "EE", "eesti"),
	Locale("fi", "FI", "suomi"),
	Locale("fr", "FR", "français"),
	Locale("ga", "IE", "Gaeilge"),
	Locale("hr", "HR", "hrvatski"),
	Locale("it", "IT", "italiano"),
	Locale("lt", "LT", "lietuvių"),
	Locale("lv", "LV", "latviešu"),
	Locale("mt", "MT", "Malti"),
	Locale("nl", "NL", "Nederlands"),
	Locale("pt", "PT", "português"),
	Locale("sk", "SK", "slovenčina"),
	Locale("sl", "SI", "slovenščina"),
)

WORLD_LOCALES = (
	Locale("bg", "BG", "български"),
	Locale("en", "US", "English\x0A(US)"),
	Locale("ro", "RO", "română"),
)

LOCALES = EZ_LOCALES + WORLD_LOCALES
