
from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {
        'id': 1,
        'Nome': "Nara",
        'E-mail': "gnara15@gmail.com",
        'Tipo': "Comprador",
        'Senha': 123,
        'Status': "ativo"
    }, {
        'id': 2,
        'Nome': "Quirino",
        'E-mail': "luizfpq@ifsp.com",
        'Tipo': "Vendedor",
        'Senha': 23423,
        'Status': "ativo"
    }
]


@app.route('/users', methods=['GET'])
def get_users():
    """gets all users """
    return jsonify(users)


@app.route('/users/<int:id>', methods=['GET'])
def get_users_by_id(id):
    """ gets users by id iterating the dict """
    for user in users:
        if user.get('id') == id:
            return jsonify(user)


@app.route('/users/<int:id>', methods=['PUT'])
def edit_users_by_id(id):
    """ edit users by id """
    for index, user in enumerate(users):
        altered_user = request.get_json()
        if user.get('id') == id:
            users[index].update(altered_user)
            return jsonify(users[index])


@app.route('/users/signup', methods=['POST'])
def insert_new_user():
    """ insert users by id """
    new_user = request.get_json()
    users.append(new_user)
    return jsonify(users)


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """ soft delete users by id """
    for index, user in enumerate(users):
        altered_user = request.get_json()
        if user.get('id') == id:
            del users[index]
            users[index].update(altered_user)
            return jsonify(users[index])


app.run(port=5000, host='localhost', debug=True)
