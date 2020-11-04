from flask_restful import Resource

users = []


class UserResource(Resource):
    def get(self):
        return {'users': users}