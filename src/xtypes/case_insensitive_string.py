class CaseInsensitiveString(str):
	__slots__ = ()

	def __str__(self) -> str:
		return super().__str__().casefold()

	def __repr__(self) -> str:
		return super().__repr__().casefold()

	def __eq__(self, other: object) -> bool:
		if type(other) is str:
			return super().casefold().__eq__(other.casefold())
		return False

	def __ne__(self, other: object) -> bool:
		if type(other) is str:
			return super().casefold().__ne__(other.casefold())
		return False

	def __lt__(self, other: str) -> bool:
		return super().casefold().__lt__(other.casefold())

	def __gt__(self, other: str) -> bool:
		return super().casefold().__gt__(other.casefold())

	def __ge__(self, other: str) -> bool:
		return super().casefold().__ge__(other.casefold())

	def __le__(self, other: str) -> bool:
		return super().casefold().__le__(other.casefold())
