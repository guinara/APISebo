from flask import Flask, Blueprint, request, session
# from flask_restful import Api, Resource
# from flasgger import Swagger
from routes.users import users
from routes.books import book
from routes.admin import admin
from routes.categorias import categorias

from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
# api = Api(app)
# swagger = Swagger(app)

app.secret_key = "SenhaSecretaUOOOOU"

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(book, url_prefix='/book')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(categorias, url_prefix='/categorias')


app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def hello_world():
    return 'Bem vindo a API de SEBO online'


if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
