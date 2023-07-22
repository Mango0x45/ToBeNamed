import flask
from flask import Blueprint

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
