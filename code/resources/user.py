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
        return {'user': user.json()}


class UserResource(Resource):
    def get(self):
        return {'users': [user.json() for user in UserModel.find_all()]}
