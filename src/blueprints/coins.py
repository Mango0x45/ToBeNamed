from http import HTTPMethod

import flask
from flask import Blueprint

coins = Blueprint("coins", __name__, url_prefix="/coins")


@coins.route("/", methods=[HTTPMethod.GET])
def index() -> str:
	return flask.render_template("coins/index.html")
