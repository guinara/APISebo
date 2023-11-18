import bcrypt
from flask import Blueprint, json, request, session
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
            Users = list(db.Users.find({"Status": "Ativado"}))
            return parse_json(Users)
        return "Usuário precisa estar logado como admin", 401
    except:
        return "Usuario nao logado", 401


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
                session["Admin"] = user["Admin"]
                return "Admin logado, Bem vindo(a) "+user["Nome"], 200
            return parse_json(
                {"Erro": "Senha inválida"}), 401
    except Exception as ex:
        template = "Uma excessão do tipo {0} ocorreu. Args:\n{1!r}"
        mensagem = template.format(type(ex).__name__, ex.args)
        mensagem = parse_json({"message": mensagem})
        return mensagem, 500


@admin.route('/signup', methods=['POST'])
def insert_new_user():
    """Insere um novo usuário no MongoDB"""
    new_user = request.get_json()
    try:
        if 'Sim' in session["Admin"]:
            contador = get_contador()
            nome = new_user["Nome"]
            senha_nao_cripto = new_user["Senha"]
            salt = bcrypt.gensalt()
            senha_cripto = bcrypt.hashpw(
                senha_nao_cripto.encode('utf-8'), salt)
            senha_cripto = senha_cripto.decode('utf8').replace("'", '"')
            email = new_user["E-mail"]
            try:
                user = db.Users.find({"E-mail": email})[0]
                if user != None:
                    return parse_json({"message": "Usuário já cadastrado!"})
            except:
                dicionario = {'id': contador, 'E-mail': email, 'Nome': nome,
                              'Senha': senha_cripto, 'Status': 'Ativado', 'Admin': 'Sim'}
                usuario = json.dumps(dicionario, indent=4)
                db.Users.insert_one(dicionario)
                return usuario, 201
    except:
        return parse_json({"message": "Usuario precisa estar logado como adm para cadastro de adm"}), 401


def get_contador():
    """Pega o id de contagem"""
    conts = db.counters.find()[0]
    contador = conts["seq_value"]
    return contador
