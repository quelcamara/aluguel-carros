import sys, getopt
from flask import Flask, jsonify
from flask_restful import Api
from flask_restful_swagger import swagger
from flask_jwt_extended import JWTManager

from resources.user import (
    UserList,
    UserResource,
    UserRegister
)
from resources.car import CarRegister, CarResource, CarList, CarRental, CarReturn
from resources.carBrand import BrandRegister, BrandResource, BrandList
from resources.userLogin import UserLogin, UserLogout, TokenRefresh
from models.userType import UserType
from blacklist import BLACKLIST

opts, args = getopt.getopt(sys.argv[1:],"",["db=", "dbuser=", "dbpassword="])
db = 'sqlite'
user = None
password = None

for opt, arg in opts:
    if opt == '--db':
        db = arg
    if opt == '--dbuser':
        user = arg
    if opt == '--dbpassword':
        password = arg

app = Flask(__name__)
api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url="/api/carros", description="API para aluguel de carros.")
jwt = JWTManager(app)
app.secret_key = 'raquel'

if db == 'mysql':
    if not user or not password:
        raise Exception('Se --db=mysql, favor digitar valores válidos para --dbuser e --dbpassword.')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@localhost/aluguelcarros_db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aluguelcarros.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

api.add_resource(UserRegister, '/users/register')
api.add_resource(UserLogin, '/users/login')
api.add_resource(TokenRefresh, '/users/refresh')
api.add_resource(UserLogout, '/users/logout')

api.add_resource(UserResource, '/users/<int:_id>')
api.add_resource(UserList, '/users')

api.add_resource(BrandRegister, '/brands/register')
api.add_resource(BrandResource, '/brands/<int:_id>')
api.add_resource(BrandList, '/brands')

api.add_resource(CarRegister, '/cars/register')
api.add_resource(CarResource, '/cars/<int:_id>')
api.add_resource(CarList, '/cars')

api.add_resource(CarRental, '/users/<int:user_id>/cars/<int:car_id>/rental')
api.add_resource(CarReturn, '/cars/<int:car_id>/return')


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
        'Descrição': 'Este token foi revogado. Faça login novamente.',
        'Erro': 'token_revoked'
    }), 401


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity["type"] == 1:
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
    return "<h2  style=\"color:purple\">Bem vindo a Fabulosa Locadora de Carros de Luxxxo da Raquel!</h1>"


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)
