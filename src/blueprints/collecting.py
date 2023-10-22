from http import HTTPMethod

import flask
from flask import Blueprint

from xtypes import Country

collecting = Blueprint("collecting", __name__, url_prefix="/collecting")


@collecting.route("/", methods=[HTTPMethod.GET])
def index() -> str:
	return flask.render_template("collecting/index.html")


@collecting.route("/crh", methods=[HTTPMethod.GET])
def crh() -> str:
	return flask.render_template(
		"collecting/crh.html",
		countries=Country.sorted_by_locale(),
	)


@collecting.route("/vending", methods=[HTTPMethod.GET])
def vending() -> str:
	return flask.render_template("collecting/vending.html")
