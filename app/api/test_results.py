from flask import Blueprint

bp = Blueprint("test_results", __name__, url_prefix="")


@bp.route("/")
def index():
    return "Test Results!"
