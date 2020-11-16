from flask_restful import Resource, reqparse
from models.user import UserModel
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
            return {'users': [user.json() for user in UserModel.find_by_type(data['user_type_filter'])]}, 200


class UserResource(Resource):
    @jwt_required
    def get(self, _id):
        claims = get_jwt_claims()
        if not claims['funcionario']:
            return {'Mensagem': 'Privilégio de administrador exigido.'}, 401

        user = UserModel.find_by_id(_id)
        if not user:
            return {'Mensagem': 'Usuário não encontrado.'}, 404
        return user.json(), 200

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
