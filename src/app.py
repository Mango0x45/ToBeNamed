import urllib.parse
from http import HTTPMethod
from typing import Any

import flask
from flask import Flask, Response
from flask_babel import Babel

import blueprints
import config
from config import Cookie


def get_locale() -> str:
	r = flask.request
	return (
		r.cookies.get(Cookie.LOCALE)
		or r.accept_languages.best_match(config.AVAILABLE_LOCALES)
		or "en_GB"
	)


def loc_to_lang(locale: str) -> str:
	return locale.replace("_", "-")


app = Flask(__name__)
babel = Babel(app, locale_selector=get_locale)


@app.context_processor
def inject_params() -> dict[str, Any]:
	return {"lang": loc_to_lang(get_locale())}


@app.before_request
def pre_request_hook() -> Response | None:
	def get_redirect() -> str:
		if req.endpoint == "root.set_language":
			url = urllib.parse.urlparse(req.referrer)
			return req.referrer if url.hostname == HOSTNAME else "/"
		return req.full_path or "/"

	req = flask.request
	if (
		req.method == HTTPMethod.POST
		or req.endpoint == "static"
		or Cookie.LOCALE in req.cookies.keys()
		and req.endpoint != "root.set_language"
	):
		return

	resp = flask.make_response(
		flask.render_template("languages.html", cname=Cookie.LOCALE)
	)
	resp.set_cookie(
		key=Cookie.REDIRECT,
		value=get_redirect(),
	)
	return resp


for bp in blueprints.BLUEPRINTS:
	app.register_blueprint(bp)

if __name__ == "__main__":
	HOSTNAME = "localhost"
	app.run(debug=True)
