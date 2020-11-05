from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import (
    UserResource,
    UserRegister,
    UserList,
    UserTypeList,
)
from resources.car import CarRegister, CarList
from resources.userLogin import UserLogin
from models.userType import UserType

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
app.secret_key = 'raquel'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:***REMOVED***@localhost/aluguelcarros_db'

api.add_resource(UserRegister, '/user/register')
api.add_resource(UserLogin, '/user/login')
api.add_resource(UserResource, '/user/<int:_id>')
api.add_resource(UserTypeList, '/users/<int:user_type>')
api.add_resource(UserList, '/users')
api.add_resource(CarRegister, '/car/register')
api.add_resource(CarList, '/cars')


@app.before_first_request
def create_tables():
    db.create_all()
    UserType.employee()
    UserType.client()


@app.route("/", methods=['GET'])
def root():
    return "Bem vindo a Fabulosa Locadora de Carros de Luxxxo da Raquel!"


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)
