import flask
from flask import Blueprint

news = Blueprint("news", __name__, url_prefix="/news")


@news.route("/", methods=["GET"])
def index() -> str:
	return flask.render_template("news/index.html")


@news.route("/<date>", methods=["GET"])
def article(date: str) -> str:
	return flask.render_template(f"news/{date}")
