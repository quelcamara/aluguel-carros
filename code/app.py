from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import (
    UserResource,
    UserRegister,
    UserList,
    UserTypeList,
)
from resources.car import CarRegister, CarResource, CarList
from resources.carBrand import BrandRegister, BrandResource, BrandList
from resources.userLogin import UserLogin, UserLogout, TokenRefresh
from models.userType import UserType
from blacklist import BLACKLIST

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
app.secret_key = 'raquel'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:***REMOVED***@localhost/aluguelcarros_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

api.add_resource(UserRegister, '/user/register')
api.add_resource(UserLogin, '/user/login')
api.add_resource(UserLogout, '/user/logout')
api.add_resource(TokenRefresh, '/user/refresh')

api.add_resource(UserResource, '/user/<int:_id>')
api.add_resource(UserTypeList, '/users/<int:user_type>')
api.add_resource(UserList, '/users')

api.add_resource(CarRegister, '/car/register')
api.add_resource(CarResource, '/car/<int:_id>')
api.add_resource(CarList, '/cars')

api.add_resource(BrandRegister, '/brand/register')
api.add_resource(BrandResource, '/brand/<int:_id>')
api.add_resource(BrandList, '/brands')


@app.before_first_request
def create_tables():
    db.create_all()
    UserType.employee()
    UserType.client()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'Descrição': 'Este token foi revogado.',
        'Erro': 'token_revoked'
    }), 401


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity["id"] == 1:
        return {'funcionario': True}
    return {'funcionario': False}


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'Descrição': 'Requisição não contém um token de acesso.',
        'Erro': 'Autorização necessária.'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'Descrição': 'Assinatura de verificação inválida. Insira um token válido.',
        'Erro': 'invalid_token'
    }), 401


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'Descrição': 'Seu token expirou. Atualize sua autenticação',
        'Erro': 'token_expired.'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'Descrição': 'Necessário um fresh token para esta ação. Faça login novamente.',
        'Erro': 'fresh_token_required'
    }), 401


@app.route("/", methods=['GET'])
def root():
    return "Bem vindo a Fabulosa Locadora de Carros de Luxxxo da Raquel!"


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)
