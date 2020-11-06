from werkzeug.security import safe_str_cmp
from flask_restful import reqparse, Resource
from flask_jwt_extended import create_access_token, create_refresh_token

from models.user import UserModel

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
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.user_type, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {'Mensagem': 'Credenciais inválidas'}, 401
