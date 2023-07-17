from typing import Mapping

import flask
from flask import Flask
from flask_babel import Babel

AVAILABLE_LOCALES = {"en_GB", "en_US"}


def get_locale() -> str:
	return flask.request.accept_languages.best_match(AVAILABLE_LOCALES) or "en_GB"


app = Flask(__name__)
babel = Babel(app, locale_selector=get_locale)


@app.context_processor
def inject_params() -> Mapping[str, any]:
	return {
		"lang": get_locale().replace("_", "-"),
	}


@app.route("/", methods=["GET"])
def index() -> str:
	return flask.render_template("index.html")


if __name__ == "__main__":
	app.run(debug=True)
