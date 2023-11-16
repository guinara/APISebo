from flask import Flask, Blueprint, request, session
# from flask_restful import Api, Resource
# from flasgger import Swagger
from routes.users import users
from routes.books import book
from routes.admin import admin
from routes.categorias import categorias


app = Flask(__name__)
# api = Api(app)
# swagger = Swagger(app)


# class InicioAPI(Resource):
#     def get(self):
#         """
#         Inicio da api com a documentação
#         ---
#         responses:
#           200:
#             description: OK
#         """
#         return {'hello': 'world'}


# api.add_resource(InicioAPI, '/inicio')
# app.secret_key = os.environ.get('secret_key')
app.secret_key = "SenhaSecretaUOOOOU"

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(book, url_prefix='/book')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(categorias, url_prefix='/categorias')


@app.route('/')
def hello_world():
    return 'Bem vindo a API de SEBO online'


if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
