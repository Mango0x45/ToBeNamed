from http import HTTPMethod

import flask
from flask import Blueprint

from xtypes import CaseInsensitiveString

notes = Blueprint("notes", __name__, url_prefix="/notes")


@notes.route("/", methods=[HTTPMethod.GET])
def index() -> str:
	return flask.render_template("notes/index.html")


@notes.route("/codes", methods=[HTTPMethod.GET])
def codes() -> str:
	return flask.render_template("notes/codes.html")


@notes.route("/designs", methods=[HTTPMethod.GET])
@notes.route("/designs/<ci_str:series>", methods=[HTTPMethod.GET])
def designs(series: CaseInsensitiveString | None = None) -> str:
	return flask.render_template(f"notes/designs/{series or 'index'}.html")


@notes.route("/test", methods=[HTTPMethod.GET])
def test() -> str:
	raise NotImplementedError
