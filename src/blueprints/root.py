import flask
from flask import Blueprint

root_bp = Blueprint("root", __name__, url_prefix="/")


@root_bp.route("/", methods=["GET"])
def index() -> str:
	return flask.render_template("index.html")


@root_bp.route("/jargon", methods=["GET"])
def jargon() -> str:
	return flask.render_template("jargon.html")


@root_bp.route("/about", methods=["GET"])
def about() -> str:
	return flask.render_template("about.html")
