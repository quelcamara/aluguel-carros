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
                         required=True,
                         default=None
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

    def delete(self):
        pass


class CarResource(Resource):
    def get(self, _id):
        car = CarModel.find_by_id(_id)
        return car.json()


class CarList(Resource):
    def get(self):
        pass


class CarBrandList(Resource):
    def get(self):
        pass