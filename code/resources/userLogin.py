from werkzeug.security import safe_str_cmp
from flask_restful import reqparse, Resource
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                get_raw_jwt,
                                jwt_refresh_token_required,
                                get_jwt_identity, jwt_required
                                )
from flask_restful_swagger import swagger
from models.swaggerModels import UsersLogin

from models.user import UserModel
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help='Este campo deve ser preenchido'
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help='Este campo deve ser preenchido'
                          )


class UserLogin(Resource):
    """Login de usuários
    Login de usuários cadastrados.
    """
    @swagger.operation(
        summary="Login de usuários cadastrados.",
        notes="Para acessar a os endpoints da api, é necessário realizar login."
              "Para que seja feito login com sucesso, o usuário precisa ter sido previamente cadastrado.",
        nickname="loginUsarios",
        parameters=[
            {
                "name": "body",
                "in": "body",
                "description": "Credenciais de acesso do usuário",
                "required": True,
                "allowMultiple": False,
                "dataType": UsersLogin.__name__,
                "paramType": "body"
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
            }
        ]
    )
    def post(self):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.json(), fresh=True)
            refresh_token = create_refresh_token(user.json())
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {'Mensagem': 'Credenciais inválidas'}, 401


class UserLogout(Resource):
    """Logout de usuários
    Logout de usuários cadastrados.
    """
    @swagger.operation(
        summary="Logout de usuários cadastrados.",
        notes="Ao fazer o logout, o usuário perde acesso aos endpoints e deixa o sistema. "
              "Para respostas válidas, inserir 'Bearer' seguido do token de acesso gerado ao realizar o login.",
        nickname="logoutUsarios",
        parameters=[
            {
                "name": "authorization",
                "in": "body",
                "description": "Autenticação de usuário.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Bearer {{access_token}}",
                "paramType": "header"
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
            }
        ]
    )
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'Mensagem': 'Logout realizado com sucesso'}, 200


class TokenRefresh(Resource):
    """Token Refresh para usuários logados
    Atualização do token de acesso.
    """
    @swagger.operation(
        summary="Gera um novo token de acesso aos usuários logados.",
        notes="Um novo access token é gerado sem a necessidade de realizar login novamente. "
              "O novo access token gerado não é 'fresh'.",
        nickname="tokenRefresh",
        parameters=[
            {
                "name": "authorization",
                "in": "body",
                "description": "Autenticação de usuário.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Bearer {{access_token}}",
                "paramType": "header"
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
            }
        ]
    )
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
