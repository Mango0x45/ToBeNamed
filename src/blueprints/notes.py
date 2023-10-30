from http import HTTPMethod

import flask
from flask import Blueprint

notes = Blueprint("notes", __name__, url_prefix="/notes")


@notes.route("/", methods=[HTTPMethod.GET])
def index() -> str:
	return flask.render_template("notes/index.html")


@notes.route("/codes", methods=[HTTPMethod.GET])
def codes() -> str:
	raise NotImplementedError


@notes.route("/designs", methods=[HTTPMethod.GET])
def designs() -> str:
	raise NotImplementedError


@notes.route("/test", methods=[HTTPMethod.GET])
def test() -> str:
	raise NotImplementedError
