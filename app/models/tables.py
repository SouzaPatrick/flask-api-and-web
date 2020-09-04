#!/usr/bin/python
# -*- coding: utf-8 -*-

from app.ext.database import db

from flask import current_app
import datetime
import pytz

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# Modelo da tabela "Papel do usuario"
class Role(db.Model):
    __tablename__ = 'role'  # Nome da tabela no banco

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    name = db.Column(db.String(100))  # "Nome" do papel/funcao
    # Coluna principal para a pesquisa de permissao, a maioria dos usuarios terao essa permissao como padrao
    default = db.Column(db.Boolean, default=False, index=True)  
    permissions = db.Column(db.Integer)

    # Relacionar os dados da aula levando em consideração o id obtido
    users = db.relationship("User", backref="role", lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)

        if self.permissions is None:
            self.permissions = 0
    
    #Adicionar novas permissoes ao papel
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm
    
    #Remover permissoes
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm
    
    #Resetar_permissoes
    def reset_permission(self):
        self.permissions = 0

    #Verifica se as permissoes combinadas inclui a permissao base
    def has_permission(self, perm):
        return self.permissions & perm == perm

    # Representação das consultas no banco, como irão ser apresentadas
    def __repr__(self):
        return "<Role %r>" % self.name

class User(db.Model):
    __tablename__ = 'user'  # Nome da tabela no banco

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now(
        pytz.timezone("America/Sao_Paulo")))
    last_seen = db.Column(db.DateTime)
    first_seen = db.Column(db.DateTime)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))


    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    # Token para sessao
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)

        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        return True

    # API
    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)

        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None

        return User.query.get(data['id'])

    #permissao de acesso
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)
    
    def is_administrator(self):
        return self.can(Permission.ADMIN)

    # Representação das consultas no banco, como irão ser apresentadas
    def __repr__(self):
        return "<User %r>" % self.username

class Permission:
    COMMENT = 1 #Criar novos comentarios
    REPLAY = 2 #Responder comentarios
    DELETE = 4 #Apagar comentarios
    MODERATE = 8 # Fazer tudo na sala
    ADMIN = 16 # Pode fazer tudo no sistema