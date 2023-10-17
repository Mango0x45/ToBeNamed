from http import HTTPMethod

import flask
from flask import Blueprint

import util

collecting = Blueprint("collecting", __name__, url_prefix="/collecting")


@collecting.route("/", methods=[HTTPMethod.GET])
def index() -> str:
	return flask.render_template("collecting/index.html")


@collecting.route("/crh", methods=[HTTPMethod.GET])
def crh() -> str:
	return flask.render_template(
		"collecting/crh.html",
		countries=util.countries_by_locale(),
	)
