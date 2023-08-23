import json
from http import HTTPMethod
from typing import NamedTuple

import flask
import flask_babel
from flask import Blueprint

import util
from util import _
from xtypes import COIN_DENOMINATIONS, COUNTRIES, MintageCoin, MintageJson, CoinType

coins = Blueprint("coins", __name__, url_prefix="/coins")


@coins.route("/", methods=[HTTPMethod.GET])
def index() -> str:
	return flask.render_template("coins/index.html")


@coins.route("/mintages", methods=[HTTPMethod.GET])
def mintages() -> str:
	def fmt(n: int) -> str:
		match n:
			case -1:
				return _("Unknown")
			case 0:
				return "—"
			case _:
				return flask_babel.format_number(n)

	def mintage(x: MintageCoin) -> int:
		s = 0
		u = True

		if opts.ifc:
			s += max(x["ifc"], 0)
			u = u and x["ifc"] == -1
		if opts.nifc:
			s += max(x["nifc"], 0)
			u = u and x["nifc"] == -1
		if opts.proof:
			s += max(x["proof"], 0)
			u = u and x["proof"] == -1

		return -1 if u else s

	def displayable(x: dict[str, str]) -> dict[CoinType, str]:
		return {
			CoinType.IFC: x["ifc"],
			CoinType.NIFC: x["nifc"],
			CoinType.PROOF: x["proof"],
		}

	Options = NamedTuple(
		"Options", (("ifc", bool), ("nifc", bool), ("proof", bool))
	)
	opts = Options(
		ifc="ifc" in flask.request.args,
		nifc="nifc" in flask.request.args,
		proof="proof" in flask.request.args,
	)

	if not opts.ifc and not opts.nifc and not opts.proof:
		opts = Options(ifc=True, nifc=False, proof=False)

	# Assert that the user hasn’t just passed garbage data through the URL
	country = (
		c if (c := flask.request.args.get("c")) in COUNTRIES else COUNTRIES[0]
	)

	# TODO: Error handling
	with open(util.from_root(f"data/mintages/{country}.json"), "r") as f:
		data: MintageJson = json.loads(f.read())

	detailed = []
	for k, v in data.items():
		row = tuple(
			{
				"ifc": fmt(x["ifc"]),
				"nifc": fmt(x["nifc"]),
				"proof": fmt(x["proof"]),
			}
			for x in v
		)
		renamed = tuple(map(displayable, row))
		detailed.append((k, *renamed))

	rows = []
	for k, v in data.items():
		row = tuple(fmt(mintage(x)) for x in v)
		rows.append((k, *row))

	return flask.render_template(
		"coins/mintages.html",
		country=country,
		countries=COUNTRIES,
		denoms=COIN_DENOMINATIONS,
		rows=rows,
		detailed=detailed,
		opts=opts,
	)
