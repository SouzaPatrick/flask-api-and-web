from flask import Blueprint

from flask_restful_swagger_2 import Api

from .home.routes import HomeAdmResource, HomeResource, HomeTeacherResource
from .auth.routes import AuthResource
from .registration.routes import RegistrationUser

bp = Blueprint("api", __name__, static_folder='static', url_prefix="/v1")
api = Api(bp)

def init_app(app):
    # Home
    api.add_resource(HomeAdmResource, "/home/adm/")
    api.add_resource(HomeTeacherResource, "/home/teacher/")
    api.add_resource(HomeResource, "/home/")

    # Auth
    api.add_resource(AuthResource, "/token/")

    # Cadastro de usuario
    api.add_resource(RegistrationUser, "/registration/")

    app.register_blueprint(bp)