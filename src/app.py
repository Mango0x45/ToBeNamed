import os.path
from typing import Mapping

import flask
from flask import Blueprint, Flask
from flask_babel import Babel
from watchdog.observers import Observer

import article_watcher
import blueprints

AVAILABLE_LOCALES = {"en_GB", "en_US"}


def get_locale() -> str:
	return flask.request.accept_languages.best_match(AVAILABLE_LOCALES) or "en_GB"


def loc_to_lang(locale: str) -> str:
	return locale.replace("_", "-")


app = Flask(__name__)
babel = Babel(app, locale_selector=get_locale)


@app.context_processor
def inject_params() -> Mapping[str, any]:
	return {"lang": loc_to_lang(get_locale())}


def setup_watcher() -> None:
	path = os.path.join(os.path.dirname(__file__), "templates/news/articles")
	article_watcher.watcher.init_articles(path)
	observer = Observer()
	observer.schedule(article_watcher.watcher, path=path)
	observer.start()


for bp in blueprints.BLUEPRINTS:
	app.register_blueprint(bp)

if __name__ == "__main__":
	setup_watcher()
	app.run(debug=True)
