import json
from flask import Flask, request
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import json_util
import urllib.parse


def parse_json(data):
    return json.loads(json_util.dumps(data))


# APIKey = 'qCLhKKgjcuhDM16reW2cdjAYmBHO9csVC8gUU8eyM63nq1Gl2MpUPNZNO0zyTWQY'
uri = 'mongodb+srv://user:password415@sebopdw.0dlksoe.mongodb.net/'

client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
db = client['Sebo']

app = Flask(__name__)


@app.route('/users', methods=['GET'])
def get_users():
    """gets all Users """
    Users = list(db.Users.find())
    return parse_json(Users)


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
    db.Users.insert_one(new_user)
    return parse_json({"message": "Usuario inserido com sucesso"})


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """Exclui um usuário por ID no MongoDB"""
    db.Users.update_one({"id": id}, {"$set": {"Status": "Desativado"}})
    return parse_json({"message": "Usuario excluído com sucesso"})


@app.route('/')
def hello_world():
    return 'Bem vindo a API de SEBO online, consulte documentação para endpoints!'


if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
