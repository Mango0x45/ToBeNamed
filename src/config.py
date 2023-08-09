from enum import EnumMeta, StrEnum
from typing import Any, NamedTuple

from util import _


class Cookie(StrEnum):
	LOCALE = "locale"
	REDIRECT = "redirect"
	THEME = "theme"


class Theme(StrEnum):
	DARK = "dark"
	LIGHT = "light"
