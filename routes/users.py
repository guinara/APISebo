import json
import os
from flask import Blueprint, request, session
import pymongo
from pymongo.server_api import ServerApi
from bson import json_util
import bcrypt

import urllib.parse
def parse_json(data):
    return json.loads(json_util.dumps(data))

users = Blueprint('users', __name__, static_folder=None)

# uri=os.environ.get('MONGODB_URI')
uri = 'mongodb+srv://user:password415@sebopdw.0dlksoe.mongodb.net/'

client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
db = client['Sebo']


@users.route('/<int:id>', methods=['GET'])
def get_users_by_id(id):
    """ gets Users by id iterating the dict """
    user = db.Users.find_one({"id": id})
    return parse_json(user)


@users.route('/<int:id>', methods=['PUT'])
def edit_users_by_id(id):
    """ edit Users by id """
    updated_user = request.get_json()
    db.Users.update_one({"id": id}, {"$set": updated_user})
    return parse_json({"message": "Usuario atualizado com sucesso"})


@users.route('/signup', methods=['POST'])
def insert_new_user():
    """Insere um novo usuário no MongoDB"""
    new_user = request.get_json()
    contador = get_contador()
    nome = new_user["Nome"]
    senha_nao_cripto = new_user["Senha"]
    salt = bcrypt.gensalt()
    senha_cripto = bcrypt.hashpw(senha_nao_cripto.encode('utf-8'), salt)
    senha_cripto = senha_cripto.decode('utf8').replace("'", '"')
    email = new_user["E-mail"]
    try:
        user = db.Users.find({"E-mail": email})[0]
        if user != None:
            return "Usuário já cadastrado!"
    except:
        tipo = new_user["Tipo"]
        dicionario = {'id': contador, 'E-mail': email, 'Nome': nome,
                      'Senha': senha_cripto, 'Status': 'Ativado', 'Tipo': tipo}
        usuario = json.dumps(dicionario, indent=4)
        db.Users.insert_one(dicionario)
        return usuario


@users.route('/login', methods=['POST'])
def login_user():
    """Cria sessão"""
    login = request.get_json()
    mail = login["E-mail"]
    try:
        user = db.Users.find({"E-mail": mail})[0]
        if user != None:
            passou = bcrypt.checkpw(login["Senha"].encode('utf-8'),
                                    user["Senha"].encode('utf-8'))
            if passou:
                session["E-mail"] = user["E-mail"]
                return "Usuário logado, Bem vindo(a) "+user["Nome"]
    except Exception as ex:
        template = "Uma excessão do tipo {0} ocorreu. Args:\n{1!r}"
        menssagem = template.format(type(ex).__name__, ex.args)
        return menssagem


@users.route('/logout', methods=['POST'])
def logout_user():
    """Encerra sessão"""
    session.pop("E-mail", None)
    session.pop("Admin", None)
    return "Usuário deslogado"


@users.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    """Exclui um usuário por ID no MongoDB"""
    db.Users.update_one({"id": id}, {"$set": {"Status": "Desativado"}})
    return parse_json({"message": "Usuario excluído com sucesso"})


def get_contador():
    """Pega o id de contagem"""
    conts = db.counters.find()[0]
    contador = conts["seq_value"]
    return contador
