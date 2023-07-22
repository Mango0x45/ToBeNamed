from http import HTTPMethod, HTTPStatus

import flask
from flask import Blueprint, Response

import config
from config import Cookie

root = Blueprint("root", __name__, url_prefix="/")


@root.route("/", methods=["GET"])
def index() -> str:
	return flask.render_template("index.html")


@root.route("/jargon", methods=["GET"])
def jargon() -> str:
	return flask.render_template("jargon.html")


@root.route("/about", methods=["GET"])
def about() -> str:
	return flask.render_template("about.html")


@root.route("/set-language", methods=[HTTPMethod.GET, HTTPMethod.POST])
def set_language() -> Response | tuple[str, HTTPStatus]:
	r = flask.request

	try:
		loc = r.form[Cookie.LOCALE]
		assert loc in config.AVAILABLE_LOCALES
	except KeyError:
		return '"locale" key missing from request form', HTTPStatus.BAD_REQUEST
	except AssertionError:
		return f'Locale "{loc}" is not an available locale', HTTPStatus.BAD_REQUEST  # type: ignore

	url = r.cookies.get(Cookie.REDIRECT, default="/")
	resp = flask.make_response(flask.redirect(url))
	resp.delete_cookie(Cookie.REDIRECT)
	resp.set_cookie(key=Cookie.LOCALE, value=loc, max_age=2**31 - 1)

	return resp
