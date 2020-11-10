from flask_restful import Resource
from models.car import CarModel


class CarRental(Resource):
    def patch(self, car_id, user_id):
        car = CarModel.find_by_id(car_id)
        if not car:
            return {'Mensagem': 'Carro não cadastrado.'}, 404

        if car.status == 'Indisponível':
            return {'Mensagem': 'Carro não disponível para aluguel.'}, 400

        if car.status == 'Disponível':
            car.status = 'Indisponível'
            car.renter = user_id

        car.save_to_db()
        return car.json()


class CarReturn(Resource):
    def patch(self, car_id):
        car = CarModel.find_by_id(car_id)
        if not car:
            return {'Mensagem': 'Carro não cadastrado.'}, 404

        if car.status == 'Disponível':
            return {'Mensagem': 'Carro indisponível para retorno.'}, 400

        if car.status == 'Indisponível':
            car.status = 'Disponível'
            car.renter = None

        car.save_to_db()
        return car.json()
