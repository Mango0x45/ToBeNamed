from typing import Any

import flask
from flask import Flask
from flask_babel import Babel

import blueprints

AVAILABLE_LOCALES = {"en_GB", "en_US"}


def get_locale() -> str:
	return flask.request.accept_languages.best_match(AVAILABLE_LOCALES) or "en_GB"


def loc_to_lang(locale: str) -> str:
	return locale.replace("_", "-")


app = Flask(__name__)
babel = Babel(app, locale_selector=get_locale)


@app.context_processor
def inject_params() -> dict[str, Any]:
	return {"lang": loc_to_lang(get_locale())}


for bp in blueprints.BLUEPRINTS:
	app.register_blueprint(bp)

if __name__ == "__main__":
	app.run(debug=True)
