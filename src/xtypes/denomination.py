import flask_babel


class Denomination(float):
	"""
	A light wrapper around a float that represents a denomination.
	"""

	__slots__ = ()

	def __str__(self) -> str:
		"""
		Return the denomination formatted in the users locale.
		"""
		return flask_babel.format_currency(super().__str__(), "EUR")


COIN_DENOMINATIONS = (
	Denomination(0.01),
	Denomination(0.02),
	Denomination(0.05),
	Denomination(0.10),
	Denomination(0.20),
	Denomination(0.50),
	Denomination(1.00),
	Denomination(2.00),
)
