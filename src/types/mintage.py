from typing import Literal

MintageCoin = dict[Literal["ifc"] | Literal["nifc"] | Literal["proof"], int]
MintageYear = list[MintageCoin]
MintageJson = dict[str, MintageYear]
