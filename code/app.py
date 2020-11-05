from flask import Flask
from flask_restful import Api

from resources.user import UserResource, UserRegister, UserList, UserTypeList
from models.userType import UserType

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:***REMOVED***@localhost/aluguelcarros_db'

api.add_resource(UserRegister, '/user/register')
api.add_resource(UserResource, '/user/<int:_id>')
api.add_resource(UserTypeList, '/users/<int:user_type>')
api.add_resource(UserList, '/users')


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
