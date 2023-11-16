import json
from flask import Flask, Blueprint, request, session
import pymongo
from pymongo.server_api import ServerApi
from .users import parse_json
from .books import get_next_sequence


categorias = Blueprint('categorias', __name__)
# uri=os.environ.get('MONGODB_URI')
uri = 'mongodb+srv://user:password415@sebopdw.0dlksoe.mongodb.net/'

client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
db = client['Sebo']


@categorias.route('/<int:id>', methods=['GET'])
def get_categorias_by_id(id):
    """ gets categorias by id iterating the dict """
    categoria = db.categorias.find_one({"IDCategoria": id, "Status": "Ativo"})
    return parse_json(categoria)


@categorias.route('/', methods=['GET'])
def get_categorias():
    """ gets categorias by id iterating the dict """
    categorias = list(db.categorias.find({"Status": "Ativo"}))
    return parse_json(categorias)


# @categorias.route('/search', methods=['GET'])
# def get_searched_itens(id):
#     """ gets categorias by search """
#     categorias = list(db.Books.find())
#     return parse_json(categorias)


@categorias.route('/<int:id>', methods=['PUT'])
def edit_categorias_by_id(id):
    """ edit categorias by id """
    updated_categoria = request.get_json()
    db.categorias.update_one({"IDCategoria": id}, {"$set": updated_categoria})
    return parse_json({"message": "categoria atualizado com sucesso"})


@categorias.route('/', methods=['POST'])
def insert_new_categoria():
    """Insere um novo usuário no MongoDB"""
    new_categoria = request.get_json()
    dicionario = {
        'IDCategoria': get_next_sequence('IDCategoria'),
        "Status": "Ativo",
        'Categoria': new_categoria["Categoria"],
        'Descricao': new_categoria["Descricao"]
    }
    usuario = json.dumps(dicionario, indent=4)
    db.categorias.insert_one(dicionario)
    return usuario


@categorias.route('/<int:id>', methods=['DELETE'])
def delete_categoria(id):
    """Exclui um usuário por ID no MongoDB"""
    db.categorias.update_one({"IDCategoria": id}, {
                             "$set": {"Status": "Desativado"}})
    return parse_json({"message": "categoria excluída com sucesso"})
