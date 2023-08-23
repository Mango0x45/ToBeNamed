from enum import StrEnum

from util import _


class CoinType(StrEnum):
	"""
	A simple enum so that we can translate these coin types properly.
	"""
	IFC = _("IFC")
	NIFC = _("NIFC")
	PROOF = _("Proof")
