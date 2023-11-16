import json
from flask import Flask, Blueprint, request, session
import pymongo
from pymongo import ReturnDocument
from pymongo.server_api import ServerApi
from .users import parse_json

book = Blueprint('book', __name__)

# uri=os.environ.get('MONGODB_URI')
uri = 'mongodb+srv://user:password415@sebopdw.0dlksoe.mongodb.net/'

client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
db = client['Sebo']


@book.route('/<int:id>', methods=['GET'])
def get_books_by_id(id):
    """ gets books by id iterating the dict """
    item = db.Books.find_one({"IDItem": id})
    if item is not None:
        return parse_json(item), 200
    return parse_json({"Erro": "Item não encontrado."}), 404


@book.route('/', methods=['GET'])
def get_books():
    """ gets books by id iterating the dict """
    Books = list(db.Books.find({"Status": "Ativado"}))
    return parse_json(Books)


@book.route('/search', methods=['GET'])
def get_searched_itens():
    """ gets books by search """
    query = request.args
    Autor = query.get("Autor")
    Titulo = query.get("Titulo")
    Books = None
    if None not in (Autor, Titulo):
        Books = list(db.Books.find({"Titulo": {'$regex': Titulo, '$options': 'i'}, "Autor": {
                     '$regex': Autor, '$options': 'i'}, "Status": "Ativado"}))
        return parse_json(Books), 200
    elif Autor is not None:
        Books = list(db.Books.find(
            {"Autor": {'$regex': Autor, '$options': 'i'}, "Status": "Ativado"}))
        return parse_json(Books), 200
    elif Titulo is not None:
        Books = list(db.Books.find(
            {"Titulo": {'$regex': Titulo, '$options': 'i'}, "Status": "Ativado"}))
        return parse_json(Books), 200
    elif Autor and Titulo is None:
        return parse_json({"Message": "Pesquise um parametro"}), 404
    else:
        return parse_json({"Erro": "Item não encontrado."}), 404


@book.route('/<int:id>', methods=['PUT'])
def edit_books_by_id(id):
    """ edit books by id """
    updated_item = request.get_json()
    db.Books.update_one({"IDItem": id}, {"$set": updated_item})
    return parse_json({"message": "Item atualizado com sucesso"}), 200


@book.route('/', methods=['POST'])
def insert_new_item():
    """Insere um novo usuário no MongoDB"""
    new_item = request.get_json()
    try:
        dicionario = {'IDItem': get_next_sequence("itemid"),
                      'Titulo': new_item["Titulo"],
                      'Autor': new_item["Autor"],
                      'Status': 'Ativado',
                      'Categoria': new_item["Categoria"],
                      'pageCount': new_item["PageCount"],
                      'Preco': new_item["Preco"],
                      'Sinopse': new_item["Sinopse"],
                      'Data de edicao': new_item["Data de edicao"]
                      }
        usuario = json.dumps(dicionario, indent=4)
    except:
        return parse_json({"message": "Erro"}), 400
    db.Books.insert_one(dicionario)
    return usuario, 200


@book.route('/<int:id>', methods=['POST'])
def insert_new_item_with_id(id):
    item = db.Books.find_one({"IDItem": id})
    if item is not None:
        return parse_json({"message": "Item já existente"}), 404
    new_item = request.get_json()
    dicionario = {'IDItem': id,
                  'Titulo': new_item["Titulo"],
                  'Autor': [new_item["Autor"]],
                  'Status': 'Ativado',
                  'Categoria': new_item["Categoria"],
                  'pageCount': new_item["PageCount"],
                  'Preco': new_item["Preco"],
                  'Sinopse': new_item["Sinopse"],
                  'Data de edicao': new_item["Data de edicao"]
                  }
    usuario = json.dumps(dicionario, indent=4)
    db.Books.insert_one(dicionario)
    return usuario, 200


def get_next_sequence(name):
    ret = db.counters.find_one_and_update({'id': name},
                                          {'$inc': {'seq': 1}}, return_document=ReturnDocument.AFTER)
    return ret['seq']


@book.route('/<int:id>', methods=['DELETE'])
def delete_item(id):
    """Exclui um usuário por ID no MongoDB"""

    db.Books.find_one_and_update(
        {"IDItem": id}, {"$set": {"Status": "Desativado"}})
    item = db.Books.find({"IDItem": id})
    return parse_json(item)
