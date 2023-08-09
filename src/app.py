import os.path
import sys
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
from config import Cookie, Theme
from xtypes.locale import EZ_LOCALES, LOCALES, WORLD_LOCALES, Locale


def get_locale() -> str:
	r = flask.request

	if not (loc := r.cookies.get(Cookie.LOCALE)) in LOCALES:
		loc = r.accept_languages.best_match(map(str, LOCALES)) or "en_GB"
	return loc


app = Flask(__name__)
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
			return req.referrer if url.hostname == HOSTNAME else "/"
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
	observer = Observer()
	observer.schedule(article_watcher.watcher, path=path)
	observer.start()


for bp in blueprints.BLUEPRINTS:
	app.register_blueprint(bp)

if __name__ == "__main__":
	debug = False
	HOSTNAME = "localhost"

	match sys.argv[1:]:
		case ["-d", s]:
			debug = True
			HOSTNAME = s
		case ["-d"]:
			debug = True
		case [s]:
			HOSTNAME = s

	setup_watcher()
	app.run(debug=debug)
