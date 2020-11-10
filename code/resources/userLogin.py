from werkzeug.security import safe_str_cmp
from flask_restful import reqparse, Resource
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                get_raw_jwt,
                                jwt_refresh_token_required,
                                get_jwt_identity, jwt_required
                                )

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
    @classmethod
    def post(cls):
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
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'Mensagem': 'Logout realizado com sucesso'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
