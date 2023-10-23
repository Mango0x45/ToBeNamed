import json
import logging
from http import HTTPMethod
from typing import NamedTuple

import flask
import flask_babel
from flask import Blueprint
from flask_babel import _

import util
import watchers.mintages
from xtypes import (
	COIN_DENOMINATIONS,
	COUNTRIES,
	CaseInsensitiveString,
	CoinType,
	Country,
	MintageCoin,
	MintageJson,
)

coins = Blueprint("coins", __name__, url_prefix="/coins")


@coins.route("/", methods=[HTTPMethod.GET])
def index() -> str:
	return flask.render_template("coins/index.html")


@coins.route("/designs", methods=[HTTPMethod.GET])
@coins.route("/designs/<ci_str:code>", methods=[HTTPMethod.GET])
def designs(code: CaseInsensitiveString | None = None) -> str:
	if code is not None:
		return flask.render_template(f"coins/designs/{code}.html", code=code)

	return flask.render_template(
		"coins/designs/index.html",
		countries=Country.sorted_by_locale(),
	)


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
	try:
		country = COUNTRIES[COUNTRIES.index(flask.request.args.get("c"))]
	except ValueError:
		country = COUNTRIES[0]

	try:
		data = watchers.mintages.watcher.mintages[country.iso_3166_1]
	except KeyError as e:
		logging.root.exception(e)
		data = {}

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
		countries=Country.sorted_by_locale(),
		denoms=COIN_DENOMINATIONS,
		rows=rows,
		detailed=detailed,
		opts=opts,
	)


@coins.route("/varieties", methods=[HTTPMethod.GET])
@coins.route("/varieties/<ci_str:code>/<name>", methods=[HTTPMethod.GET])
def varieties(
	code: CaseInsensitiveString | None = None, name: str | None = None
) -> str:
	if code is not None and name is not None:
		return flask.render_template(f"coins/varieties/{code}/{name}.html")
	if code is not None or name is not None:
		logging.root.warning(f"Got {code=} and {name=}; should be unreachable")

	return flask.render_template(
		"coins/varieties/index.html",
		countries=Country.sorted_by_locale(),
	)
