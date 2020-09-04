#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import pytz

# Import tables e schemas
from app.models.tables import User as UserTable

#Integratios
from app.integration.role import Role


class User:
    def insert(self, data, db):
        createdOn = datetime.datetime.now(pytz.timezone("America/Sao_Paulo"))

        # Cria uma instância da classe person utilizando os dados do post
        _user = UserTable(
            username=data['username'], password=data['password'], 
            role_id=data['role_id'], created_on=createdOn)

        # Enquanto um usuário tiver usando minha aplicação ele usa essa sessão
        db.session.add(_user)  # Adiciona os dados no banco
        db.session.commit()  # Serve para o salvamento de informações

        return _user
    
    def check_first_seen(self, id):
        # Cria uma instância da classe user utilizando os dados do post
        _user = self.get_by_id(id)

        if _user.first_seen != None:
            return False
        else:
            return True


    def first_seen(self, id, datetime, db):
        # Cria uma instância da classe person utilizando os dados do post
        _user = self.get_by_id(id)

        # Enquanto um usuário tiver usando minha aplicação ele usa essa sessão
        _user.first_seen = datetime  # Altero o estado para ativo no banco de dados
        db.session.commit()  # Serve para o salvamento de informações

        return _user


    def last_seen(self, id, datetime, db):
        # Cria uma instância da classe person utilizando os dados do post
        _user = self.get_by_id(id)

        # Enquanto um usuário tiver usando minha aplicação ele usa essa sessão
        _user.last_seen = datetime  # Altero o estado para ativo no banco de dados
        db.session.commit()  # Serve para o salvamento de informações

        return _user
    
    def get_by_id(self, id):
        return UserTable.query.get(id)
