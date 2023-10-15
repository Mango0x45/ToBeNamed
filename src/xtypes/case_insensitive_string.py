from werkzeug.routing import BaseConverter


class CaseInsensitiveString(str):
	"""
	A case-insensitive string type.  Comparisons of strings of this type are
	always performed in a case-insensitive fashion.  This class should be used
	everywhere where case is not important.
	"""

	__slots__ = ()

	def __str__(self) -> str:
		return self.casefold()

	def __repr__(self) -> str:
		return repr(self.casefold())

	def __eq__(self, other: object) -> bool:
		if type(other) is str:
			return self.casefold() == other.casefold()
		return False

	def __ne__(self, other: object) -> bool:
		if type(other) is str:
			return self.casefold() != other.casefold()
		return False

	def __lt__(self, other: str) -> bool:
		return self.casefold() < other.casefold()

	def __gt__(self, other: str) -> bool:
		return self.casefold() > other.casefold()

	def __le__(self, other: str) -> bool:
		return self.casefold() <= other.casefold()

	def __ge__(self, other: str) -> bool:
		return self.casefold() >= other.casefold()


class CaseInsensitiveStringConverter(BaseConverter):
	def to_python(self, value: str) -> CaseInsensitiveString:
		return CaseInsensitiveString(value)

	def to_url(self, value: CaseInsensitiveString) -> str:
		return str(value)
