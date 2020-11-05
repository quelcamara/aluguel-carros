from flask_restful import Resource
from models.car import CarModel


class CarRegister(Resource):
    def post(self):
        return {'Mensagem': 'oi'}


class CarResource(Resource):
    pass


class CarList(Resource):
    def get(self):
        pass
