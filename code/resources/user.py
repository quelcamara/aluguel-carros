from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import jwt_required

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help='Este campo deve ser preenchido.'
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help='Este campo deve ser preenchido.'
                          )
_user_parser.add_argument('name',
                          type=str,
                          required=True,
                          help='Este campo deve ser preenchido'
                          )
_user_parser.add_argument('user_type',
                          type=int,
                          required=True,
                          help='Este campo deve ser preenchido'
                          )


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if len(data['password']) < 6:
            return {'Mensagem': 'Senha deve ter no mínimo 6 dígitos.'}, 400

        if UserModel.find_by_username(data['username']):
            return {'Mensagem': 'Usuário com username já cadastrado.'}, 400

        user = UserModel(**data)
        user.save_to_db()
        return user.json(), 201


class UserResource(Resource):
    def get(self, _id):
        user = UserModel.find_by_id(_id)
        return user.json(), 200

    def delete(self, _id):
        user = UserModel.find_by_id(_id)

        if not user:
            return {'Mensagem': 'Usuário não encontrado'}, 404

        user.delete_from_db()
        return {'Mensagem': 'Usuário excluído com sucesso.'}, 200


class UserTypeList(Resource):
    @jwt_required
    def get(self, user_type):
        return {'users': [user.json() for user in UserModel.find_by_type(user_type)]}, 200


class UserList(Resource):
    def get(self):
        return {'users': [user.json() for user in UserModel.find_all()]}, 200
