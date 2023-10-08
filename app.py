import json
from flask import Flask, request,session
import pymongo
from pymongo.server_api import ServerApi
from bson import json_util
import bcrypt

import urllib.parse


def parse_json(data):
    return json.loads(json_util.dumps(data))


uri = 'mongodb+srv://user:password415@sebopdw.0dlksoe.mongodb.net/'

client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
db = client['Sebo']

app = Flask(__name__)
app.secret_key = 'SenhaSecretaUOOOOU'


@app.route('/users', methods=['GET'])
def get_users():
    """gets all Users """
    if  'lul@ifsp.com' in session["E-mail"]:
        Users = list(db.Users.find())
        return parse_json(Users)
    print(session)
    return "Usuário precisa estar logado como admin"


@app.route('/users/<int:id>', methods=['GET'])
def get_users_by_id(id):
    """ gets Users by id iterating the dict """
    user = db.Users.find_one({"id": id})
    return parse_json(user)


@app.route('/users/<int:id>', methods=['PUT'])
def edit_users_by_id(id):
    """ edit Users by id """
    updated_user = request.get_json()
    db.Users.update_one({"id": id}, {"$set": updated_user})
    return parse_json({"message": "Usuario atualizado com sucesso"})


@app.route('/users/signup', methods=['POST'])
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


@app.route('/users/login', methods=['POST'])
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
                session["E-mail"]=user["E-mail"]
                return "Usuário logado, Bem vindo(a) "+user["Nome"]
    except:
        return "Não achou"
    
@app.route('/users/logout', methods=['POST'])
def logout_user():
    """Encerra sessão"""
    session.pop("E-mail", None)
    return "Usuário deslogado"


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """Exclui um usuário por ID no MongoDB"""
    db.Users.update_one({"id": id}, {"$set": {"Status": "Desativado"}})
    return parse_json({"message": "Usuario excluído com sucesso"})


def get_contador():
    """Pega o id de contagem"""
    conts = db.counters.find()[0]
    contador = conts["seq_value"]
    return contador


@app.route('/')
def hello_world():
    return 'Bem vindo a API de SEBO online'


if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
