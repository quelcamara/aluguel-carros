from flask_restful import Resource
from models.user import UserModel


class UserResource(Resource):
    def get(self):
        return {'users': [user.json() for user in UserModel.find_all()]}
