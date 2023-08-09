from util import _
from xtypes.case_insensitive_string import CaseInsensitiveString


class Country:
	"""
	A simple class representing a country.  Every country has two components, a
	name (such as “The Netherlands”), and an ISO 3166-1 Alpha-2 code (such as
	“NL”).
	"""

	__slots__ = ("iso_3166_1", "name")

	def __init__(self, iso_3166_1: str, name: str) -> None:
		self.iso_3166_1 = CaseInsensitiveString(iso_3166_1)
		self.name = name

	def __eq__(self, other: object) -> bool:
		"""
		Check equality between two countries.  We also want to handle the string
		case, who knows if this will ever get compared with a raw country code.
		"""
		match other:
			case Country():
				return self.iso_3166_1 == other.iso_3166_1
			case str():
				return self.iso_3166_1 == other
			case _:
				return False

	def __str__(self) -> str:
		"""
		Return the countries ISO 3166-1 Alpha-2 code.
		"""
		return self.iso_3166_1


COUNTRIES = (
	Country("ad", _("Andorra")),
	Country("at", _("Austria")),
	Country("be", _("Belgium")),
	Country("cy", _("Cyprus")),
	Country("de", _("Germany")),
	Country("ee", _("Estonia")),
	Country("es", _("Spain")),
	Country("fi", _("Finland")),
	Country("fr", _("France")),
	Country("gr", _("Greece")),
	Country("hr", _("Croatia")),
	Country("ie", _("Ireland")),
	Country("it", _("Italy")),
	Country("lt", _("Lithuania")),
	Country("lu", _("Luxembourg")),
	Country("lv", _("Latvia")),
	Country("mc", _("Monaco")),
	Country("mt", _("Malta")),
	Country("nl", _("Netherlands")),
	Country("pt", _("Portugal")),
	Country("si", _("Slovenia")),
	Country("sk", _("Slovakia")),
	Country("sm", _("San Marino")),
	Country("va", _("Vatican City")),
)
