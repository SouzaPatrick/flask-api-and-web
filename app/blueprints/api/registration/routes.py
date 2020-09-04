
from flask_restful_swagger_2 import Resource
from flask import request

from app.ext.database import db

#Autentication
from app.ext.auth_api import auth_api

#Integrations
# from app.integration.status import Status
from app.integration.role import Role
from app.integration.user import User


class RegistrationUser(Resource):
    def post(self):
        data = request.get_json()

        _user = User().insert(data=data, db=db)

        if _user:
            return 'Usuario inserido'
        
        return 'Erro ao tentar cadastrar usuario'