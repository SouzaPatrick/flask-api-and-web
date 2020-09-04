from flask import Blueprint

from .views import home, logout

bp = Blueprint("webui", __name__, template_folder="templates")

bp.add_url_rule(
    "/", view_func=home)

bp.add_url_rule(
    "/logout/", view_func=logout)


def init_app(app):
    app.register_blueprint(bp)
