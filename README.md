Campos
• ID, Nome, Email, Senha, Status (ativado/desativado), Tipo (comprador/vendedor), _id(id automático do mongoDB)
# Endpoints:
</br>

## • GET /users
mostra todos os usuarios (requer autenticação) admim: "lul@ifsp.com"
</br>

## • POST /users/signup
Registro de um usuário. (usa um input json) senhas em int causam erro
{
        "E-mail": String,
        "Nome": String,
        "Senha": String,
        "Tipo": String,
    }
    </br>
## • PUT /users/{id} - Edita informações do usuário. (usa um input json) senhas em int causam erro
{
        "E-mail": String,
        "Nome": String,
        "Senha": String,
        "Tipo": String,
    }
    </br>
## • DELETE /users/{id} - Desativa um usuário (soft delete). """
  GET /users/login
	{
        "Nome": String,
        "Senha": String,
    }
    </br>
## • GET /users/<int:id> recupera um usuário pelo id
 POST /users/login 
{
        "E-mail": String,
        "Senha": String,
    }
## • POST /users/logout 
