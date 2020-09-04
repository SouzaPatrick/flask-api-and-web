from flask_restful_swagger_2 import Resource
from flask import g, jsonify

#Autentication
from app.ext.auth_api import auth_api

#Integration
from app.integration.user import User

class AuthResource(Resource):
    @auth_api.login_required
    def get(self):
        if g.current_user.is_anonymous and not g.token_used:
            return'Usuario e senha invalidos'
            
        expiration = 5184000
        is_firstSeen = User().check_first_seen(g.current_user.id)

        return g.current_user.generate_auth_token(expiration=expiration)