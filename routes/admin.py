import bcrypt
from flask import Blueprint, request, session
from .users import parse_json
from pymongo.server_api import ServerApi
import pymongo


admin = Blueprint('admin', __name__)

# uri=os.environ.get('MONGODB_URI')
uri = 'mongodb+srv://user:password415@sebopdw.0dlksoe.mongodb.net/'

client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
db = client['Sebo']


@admin.route('/users', methods=['GET'])
def get_users():
    """gets all Users """
    try:
        if 'Sim' in session["Admin"]:
            Users = list(db.Users.find())
            return parse_json(Users)
        return "Usuário precisa estar logado como admin"
    except:
        return "Usuario nao logado"

@admin.route('/login', methods=['POST'])
def login_user():
    """Cria sessão"""
    login = request.get_json()
    mail = login["E-mail"]
    try:
        user = db.Users.find({"E-mail": mail,
                              "Admin": "Sim"})[0]
        if user != None:
            passou = bcrypt.checkpw(login["Senha"].encode('utf-8'),
                                    user["Senha"].encode('utf-8'))
            if passou:
                session["E-mail"] = user["E-mail"]
                session["Admin"] = "Sim"
                return "Admin logado, Bem vindo(a) "+user["Nome"]
    except:
        return "Não achou"
