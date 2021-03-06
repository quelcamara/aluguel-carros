from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_restful_swagger import swagger
from flask_jwt_extended import jwt_required, get_jwt_claims, fresh_jwt_required


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          case_sensitive=True,
                          required=True,
                          nullable=False,
                          help='Este campo deve ser preenchido.'
                          )
_user_parser.add_argument('password',
                          type=str,
                          case_sensitive=True,
                          required=True,
                          nullable=False,
                          help='Este campo deve ser preenchido.'
                          )
_user_parser.add_argument('name',
                          type=str,
                          required=True,
                          nullable=False,
                          help='Este campo deve ser preenchido'
                          )
_user_parser.add_argument('user_type',
                          type=int,
                          required=True,
                          choices=(1, 2),
                          nullable=False,
                          help='Tipo de usuário inválido.'
                          )

_user_parser_query = reqparse.RequestParser()
_user_parser_query.add_argument('user-type',
                                dest='user_type_filter',
                                required=False,
                                type=int,
                                choices=(1, 2),
                                location='args'
                                )


class UserRegister(Resource):
    """Registro de usuários
    Cadastro de clientes e funcionários no banco de dados.
    """
    @swagger.operation(
        summary="Registra um usuário no banco de dados.",
        notes="Para respostas válidas, todos os campos devem ser preenchidos. Não é permitido "
              "o registro de usuários usernames já em uso, password devem ter len >= 6 e"
              " deve ser inserido um valor válido para user_type {1-funcionários, 2-clientes}.",
        nickname="registroUsario",
        parameters=[
            {
                "name": "body",
                "in": "body",
                "description": "Objeto user que precisa ser adicionado.",
                "required": True,
                "dataType": UserModel.__name__,
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "Created"
            },
            {
                "code": 400,
                "message": "Bad Request"
            },
            {
                "code": 500,
                "message": "Internal Server Error"
            }
        ]
    )
    def post(self):
        data = _user_parser.parse_args()

        if len(data['password']) < 6:
            return {'Mensagem': 'Senha deve ter no mínimo 6 dígitos.'}, 400

        if UserModel.find_by_username(data['username']):
            return {'Mensagem': 'Usuário com username já cadastrado.'}, 400

        user = UserModel(**data)
        try:
            user.save_to_db()
        except:
            return {'Mensagem': 'Um erro ocorreu ao tentar salvar o usuário. Confira os dados de entrada.'}, 500

        return user.json(), 201


class UserList(Resource):
    """Lista de usuários
        Listagem de usuários cadastrados, sendo possível filtrar por tipo de usuário.
        """
    @swagger.operation(
        summary="Listagem de usuários do banco de dados.",
        notes="Se nenhum parâmetro for incluído, é retornada uma lista com todos os usuários. "
              "Caso contrário, retornará uma lista com os usuários cadastrados apenas com "
              "o tipo de usuário pesquisado. Esta é uma requisição permitida apenas "
              "para usuários do tipo 'funcionários'.",
        nickname="listaUsarios",
        parameters=[
            {
                "name": "authorization",
                "in": "body",
                "description": "Autenticação de usuário.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Bearer {{access_token}}",
                "paramType": "header"
            },
            {
                "name": "user-type",
                "in": "query",
                "description": "Filtro para tipo de usuários.",
                "required": False,
                "allowMultiple": False,
                "dataType": "1-funcionários / "
                            "2-clientes",
                "paramType": "query",
                "enum": [1, 2]
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
            {
                "code": 401,
                "message": "Unauthorized"
            },
            {
                "code": 404,
                "message": "Not Found"
            },
        ]
    )
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not claims['funcionario']:
            return {'Mensagem': 'Privilégio de administrador exigido.'}, 401

        data = _user_parser_query.parse_args()

        if data['user_type_filter'] is None:
            return {'users': [user.json() for user in UserModel.find_all()]}, 200
        elif data['user_type_filter']:
            users = UserModel.find_by_type(data['user_type_filter'])
            if not users:
                return {'Mensagem': 'Usuários não encontrados.'}, 404
            return {'users': [user.json() for user in users]}, 200


class UserResource(Resource):
    """Recursos permitidos com usuários cadastrados
   Métodos para recuperar um usuário por ID e para excluir usuário do banco de dados.
   """
    @swagger.operation(
        summary="Encontra usuário por ID.",
        notes="Retorna um único usuário. Esta é uma requisição permitida "
              "apenas para usuários do tipo 'funcionários'.",
        nickname="buscaUsarioPorID",
        parameters=[
            {
                "name": "authorization",
                "in": "body",
                "description": "Autenticação de usuário.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Bearer {{access_token}}",
                "paramType": "header"
            },
            {
                "name": "_id",
                "in": "path",
                "description": "ID do usuário para ser retornado.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Integer",
                "paramType": "path"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
            {
                "code": 401,
                "message": "Unauthorized"
            },
            {
                "code": 404,
                "message": "Not Found"
            },
        ]
    )
    @jwt_required
    def get(self, _id):
        claims = get_jwt_claims()
        if not claims['funcionario']:
            return {'Mensagem': 'Privilégio de administrador exigido.'}, 401

        user = UserModel.find_by_id(_id)
        if not user:
            return {'Mensagem': 'Usuário não encontrado.'}, 404
        return user.json(), 200

    @swagger.operation(
        summary="Exclui um cadastro de usuário.",
        notes="Para resposta válida, este endpoint deve ser testado com um fresh access token. "
              "Para isso, basta inserir o token gerado após realizado login. Token de acesso "
              "do tipo 'refresh' não é permitido para executar esta ação. Esta é "
              "uma requisição permitida apenas para usuários do tipo 'funcionários'.",
        nickname="excluiUsario",
        parameters=[
            {
                "name": "authorization",
                "in": "body",
                "description": "Autenticação de usuário.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Bearer {{access_token}}",
                "paramType": "header"
            },
            {
                "name": "_id",
                "in": "path",
                "description": "ID do cadastro de usuário a ser excluído.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Integer",
                "paramType": "path"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
            {
                "code": 401,
                "message": "Unauthorized"
            },
            {
                "code": 404,
                "message": "Not Found"
            },
        ]
    )
    @fresh_jwt_required
    def delete(self, _id):
        claims = get_jwt_claims()
        if not claims['funcionario']:
            return {'Mensagem': 'Privilégio de administrador exigido.'}, 401

        user = UserModel.find_by_id(_id)
        if not user:
            return {'Mensagem': 'Usuário não encontrado'}, 404

        user.delete_from_db()
        return {'Mensagem': 'Usuário excluído com sucesso.'}, 200
