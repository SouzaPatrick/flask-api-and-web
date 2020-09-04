from flask_httpauth import HTTPBasicAuth
from flask import g, request
from datetime import datetime
import pytz

from app.ext.database import db

# Tables
from app.models.tables import User as UserTable

# Integration
from app.integration.user import User

auth_api = HTTPBasicAuth()

@auth_api.verify_password
def verify_password(username, password):
    if request.headers.get('token'):
        _user = UserTable.verify_auth_token(request.headers.get('token'))

        if _user:
            g.current_user = UserTable.verify_auth_token(
                request.headers.get('token'))
            g.token_used = True

            # Data e hr do acesso
            datetimeNow = datetime.now(pytz.timezone("America/Sao_Paulo"))
            user = User()

            if user.check_first_seen(g.current_user.id):
                user.first_seen(g.current_user.id, datetimeNow,
                                db)  # Inserir o primeiro acesso

            user.last_seen(g.current_user.id, datetimeNow,
                           db)  # Alterar último acesso

            return g.current_user is not None

        g.current_user = None

        return g.current_user is None

    elif request.path == '/v1/token/' or request.path == '/v1/token':
        if username == '':
            return False

        _user = UserTable.query.filter_by(username=username).first()

        if _user:
            g.current_user = _user
            g.token_used = False

            # Data e hr do acesso
            datetimeNow = datetime.now(pytz.timezone("America/Sao_Paulo"))
            User().last_seen(g.current_user.id, datetimeNow,
                           db)  # Alterar último acesso


            return _user.verify_password(password)

    print(request.path)
    return False

@auth_api.error_handler
def auth_error():
    return 'Usuario e senha invalidos'


def init_app(app):
    auth_api(app)