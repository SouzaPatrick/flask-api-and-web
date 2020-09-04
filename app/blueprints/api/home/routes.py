from flask import g
# from flask_restful_swagger_2 import Resource, swagger
from flask_restful_swagger_2 import Resource

#Permission
from app.models.tables import Permission
from app.decorators import admin_required, permission_required

#Integration
from app.integration.user import User

#Autentication
from app.ext.auth_api import auth_api

class HomeAdmResource(Resource):
    @auth_api.login_required
    @admin_required
    def get(self):
        if not g.current_user is None:

            return 'ADMIN'

        return 'Token do usuario invalido'

class HomeTeacherResource(Resource):
    @auth_api.login_required
    @permission_required(Permission.MODERATE)
    def get(self):
        if not g.current_user is None:

            return 'Professor'

        return 'Token do usuario invalido'


class HomeResource(Resource):
    @auth_api.login_required
    def get(self):
        if not g.current_user is None:
            if g.current_user.is_administrator():
                return 'ADMIN'
            elif g.current_user.can(Permission.MODERATE):
                return 'Professor'
            print(g.current_user.can(Permission.MODERATE))
            return 'Usuraio sem permissao'

        return 'Token do usuario invalido'