import argparse
import logging
import os.path
import urllib.parse
from http import HTTPMethod
from typing import Any

import flask
import flask_babel
from flask import Flask, Response
from flask_babel import Babel
from watchdog.observers import Observer

import article_watcher
import blueprints
import logger
from xtypes import (
	EZ_LOCALES,
	LOCALES,
	WORLD_LOCALES,
	CaseInsensitiveStringConverter,
	Cookie,
	Locale,
	Theme,
)


class ServerArgs:
	debug: bool
	hostname: str


def get_locale() -> str:
	r = flask.request

	if not (loc := r.cookies.get(Cookie.LOCALE)) in LOCALES:
		loc = r.accept_languages.best_match(map(str, LOCALES)) or "en_GB"
	return loc


app = Flask(__name__)
app.jinja_env.policies["ext.i18n.trimmed"] = True
app.url_map.converters["ci_str"] = CaseInsensitiveStringConverter
babel = Babel(app, locale_selector=get_locale)


@app.context_processor
def inject_params() -> dict[str, Any]:
	return {
		"lang": Locale.from_str(get_locale()).as_lang(),
		"theme": flask.request.cookies.get(Cookie.THEME, Theme.DARK),
		"babel": flask_babel,
	}


@app.before_request
def pre_request_hook() -> Response | None:
	def get_redirect() -> str:
		if req.endpoint == "root.set_language":
			url = urllib.parse.urlparse(req.referrer)
			return req.referrer if url.hostname == server_args.hostname else "/"
		return req.full_path or "/"

	req = flask.request

	if (
		req.method == HTTPMethod.POST
		or req.endpoint == "static"
		or Cookie.LOCALE in req.cookies.keys()
		and req.cookies.get(Cookie.LOCALE) in LOCALES
		and req.endpoint != "root.set_language"
	):
		return

	resp = flask.make_response(
		flask.render_template(
			"languages.html",
			cname=Cookie.LOCALE,
			EZ_LOCALES=EZ_LOCALES,
			WORLD_LOCALES=WORLD_LOCALES,
		)
	)
	resp.set_cookie(
		key=Cookie.REDIRECT,
		value=get_redirect(),
	)

	# This cookie should always be set.  Obviously when the user uses the site
	# for the first time it won’t be, so we set it as they also set up their
	# language settings.
	if Cookie.THEME not in req.cookies.keys():
		resp.set_cookie(key=Cookie.THEME, value=Theme.DARK, max_age=2**31 - 1)

	return resp


def setup_watcher() -> None:
	path = os.path.join(os.path.dirname(__file__), "templates/news/articles")
	article_watcher.watcher.init_articles(path)
	app.logger.debug(f"Watching for articles in ‘{path}’")
	observer = Observer()
	observer.schedule(article_watcher.watcher, path=path)
	observer.start()
	app.logger.debug("Started article watcher")


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--debug", action="store_true")
	parser.add_argument("hostname", nargs="?", default="localhost")
	server_args = parser.parse_args(namespace=ServerArgs())

	logger.setup(server_args.debug)
	setup_watcher()

	for bp in blueprints.BLUEPRINTS:
		app.register_blueprint(bp)
		logging.root.debug(f"Registered blueprint ‘{bp.name}’")

	logging.getLogger("werkzeug").disabled = True
	app.run(debug=server_args.debug)
