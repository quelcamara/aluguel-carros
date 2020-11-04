from flask import Flask
from flask_restful import Api

from resources.user import UserResource, UserRegister, UserList

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

api.add_resource(UserRegister, '/user/register')
api.add_resource(UserList, '/users')
api.add_resource(UserResource, '/user/<string:username>')


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/", methods=['GET'])
def root():
    return "Bem vindo a Fabulosa Locadora de Carros de Luxxxo da Raquel!"


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)
