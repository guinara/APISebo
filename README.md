ENDPOINTS
Campos
• ID, Nome, Email, Senha, Status (ativado/desativado), Tipo (comprador/vendedor), _id(id automático do mongoDB)
Endpoints:

• GET /users- mostra todos os usuarios (requer autenticação) admim: "lul@ifsp.com"
• POST /users/signup - Registro de um usuário. (usa um input json) senhas em int causam erro
{
        "E-mail": String,
        "Nome": String,
        "Senha": String,
        "Tipo": String,
    }
• PUT /users/{id} - Edita informações do usuário. (usa um input json) senhas em int causam erro
{
        "E-mail": String,
        "Nome": String,
        "Senha": String,
        "Tipo": String,
    }
• DELETE /users/{id} - Desativa um usuário (soft delete). """
  GET /users/login
	{
        "Nome": String,
        "Senha": String,
    }
• GET /users/<int:id> recupera um usuário pelo id
 POST /users/login 
{
        "E-mail": String,
        "Senha": String,
    }
• POST /users/logout 