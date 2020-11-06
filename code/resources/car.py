from flask_restful import Resource
from flask_restful import reqparse
from models.car import CarModel

_user_parse = reqparse.RequestParser()
_user_parse.add_argument('name',
                         type=str,
                         required=True,
                         help='Este campo deve ser preenchido'
                         )
_user_parse.add_argument('color',
                         type=str,
                         default='-'
                         )
_user_parse.add_argument('year',
                         type=int,
                         required=True,
                         help='Este campo deve ser preenchido'
                         )
_user_parse.add_argument('daily_cost',
                         type=float,
                         required=True,
                         help='Este campo deve ser preenchido'
                         )


class CarRegister(Resource):
    def post(self):
        data = _user_parse.parse_args()
        car = CarModel(**data)
        car.save_to_db()
        return car.json(), 200


class CarResource(Resource):
    def get(self, _id):
        car = CarModel.find_by_id(_id)

        if not car:
            return {'Mensagem': 'Carro não encontrado'}, 404

        return car.json()

    def delete(self, _id):
        car = CarModel.find_by_id(_id)

        if not car:
            return {'Mensagem': 'Carro não encontrado.'}, 404

        car.delete_from_db()
        return{'Mensagem': 'Carro excluído com sucesso.'}, 200


class CarList(Resource):
    def get(self):
        return {'cars': [car.json() for car in CarModel.find_all()]}
