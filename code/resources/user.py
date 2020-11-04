from flask_restful import Resource, reqparse
from models.user import UserModel

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


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        user = UserModel(**data)
        user.save_to_db()
        return user.json(), 201


class UserResource(Resource):
    def get(self, username):
        user = UserModel.find_by_username(username)
        return user.json()


class UserList(Resource):
    def get(self):
        return {'users': [user.json() for user in UserModel.find_all()]}
