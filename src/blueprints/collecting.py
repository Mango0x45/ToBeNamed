from http import HTTPMethod

import flask
from flask import Blueprint

collecting = Blueprint("collecting", __name__, url_prefix="/collecting")


@collecting.route("/", methods=[HTTPMethod.GET])
def index() -> str:
	return flask.render_template("collecting/index.html")
