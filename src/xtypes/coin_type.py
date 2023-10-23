from enum import StrEnum

from flask_babel import _


class CoinType(StrEnum):
	"""
	A simple enum so that we can translate these coin types properly.
	"""

	IFC = _("Circulation Coin")
	NIFC = _("NIFC / BU Sets")
	PROOF = _("Proof")
