import flask
from flask import Blueprint

coins_bp = Blueprint("coins", __name__, url_prefix="/coins")


@coins_bp.route("/", methods=["GET"])
def index() -> str:
	return flask.render_template("coins/index.html")
