from typing import NamedTuple

import flask
import flask_babel
from flask import Blueprint

import watchers.articles
from watchers.articles import RawArticle


class Article(NamedTuple):
	headline: str
	iso_8601: str
	date: str


news = Blueprint("news", __name__, url_prefix="/news")


@news.route("/", methods=["GET"])
def index() -> str:
	def raw_to_article(ra: RawArticle) -> Article:
		return Article(
			headline=ra.headline,
			iso_8601=ra.date.isoformat(),
			date=flask_babel.format_date(ra.date, "short"),
		)

	articles = map(raw_to_article, watchers.articles.watcher.articles)
	return flask.render_template("news/index.html", articles=articles)


@news.route("/<date>", methods=["GET"])
def article(date: str) -> str:
	return flask.render_template(f"news/articles/{date}.html")
