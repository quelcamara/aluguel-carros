from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, fresh_jwt_required
from models.car import CarModel

_user_parse = reqparse.RequestParser()
_user_parse.add_argument('name',
                         type=str,
                         required=True,
                         nullable=False,
                         help='Este campo deve ser preenchido'
                         )
_user_parse.add_argument('color',
                         type=str,
                         default='-'
                         )
_user_parse.add_argument('year',
                         type=int,
                         required=True,
                         nullable=False,
                         help='Este campo deve ser preenchido'
                         )
_user_parse.add_argument('license_plate',
                         type=str,
                         required=True,
                         nullable=False,
                         help='Este campo deve ser preenchido'
                         )
_user_parse.add_argument('daily_cost',
                         type=float,
                         required=True,
                         nullable=False,
                         help='Este campo deve ser preenchido'
                         )
_user_parse.add_argument('brand_id',
                         type=int,
                         required=True,
                         nullable=False,
                         help='Este campo deve ser preenchido'
                         )
_user_parse.add_argument('status',
                         type=str,
                         default='Disponível',
                         nullable=False,
                         choices=('Disponível', 'Indisponível'),
                         help='Este campo deve ser preenchido os valores: <Disponível> ou <Indisponível>'
                         )

_user_parse_query = reqparse.RequestParser()
_user_parse_query.add_argument('car-year',
                               dest='car_year',
                               required=False,
                               type=int,
                               location='args'
                               )
_user_parse_query.add_argument('car-brand',
                               dest='car_brand',
                               required=False,
                               type=int,
                               location='args'
                               )
_user_parse_query.add_argument('car-status',
                               dest='car_status',
                               required=False,
                               type=str,
                               choices=('disponivel', 'indisponivel'),
                               location='args'
                               )


class CarRegister(Resource):
    @jwt_required
    def post(self):
        claims = get_jwt_claims()

        if not claims['funcionario']:
            return {'Mensagem': 'Privilégio de administrador exigido.'}, 401

        data = _user_parse.parse_args()
        car = CarModel(**data)
        try:
            car.save_to_db()
        except:
            return {'Mensagem': 'Um erro ocorreu ao tentar inserir o carro. Confira os dados de entrada.'}, 500

        return car.json(), 200


class CarList(Resource):
    @jwt_required
    def get(self):
        data = _user_parse_query.parse_args()

        if data['car_year'] is None and data['car_brand'] is None and data['car_status'] is None:
            return {'cars:', [car.json() for car in CarModel.find_all()]}, 200
        elif data['car_year']:
            cars = CarModel.find_by_year(data['car_year'])
            if not cars:
                return {'Mensagem': 'Não existem carros com este ano registrados.'}, 404
            return {'cars': [car.json() for car in cars]}, 200
        elif data['car_brand']:
            cars = CarModel.find_by_brand(data['car_brand'])
            if not cars:
                return {'Mensagem': 'Não existem carros registrados para esta marca.'}, 404
            return {'cars': [car.json() for car in cars]}, 200
        elif data['car_status']:
            cars = CarModel.find_by_status(data['car_status'])
            if not cars:
                return {'Mensagem': f'Não existem carros com este status no momento.'}, 404
            return {'cars': [car.json() for car in cars]}, 200


class CarResource(Resource):
    @jwt_required
    def get(self, _id):
        car = CarModel.find_by_id(_id)

        if not car:
            return {'Mensagem': 'Carro não encontrado'}, 404
        return car.json(), 200

    @fresh_jwt_required
    def delete(self, _id):
        claims = get_jwt_claims()
        if not claims['funcionario']:
            return {'Mensagem': 'Privilégio de administrador exigido.'}, 401

        car = CarModel.find_by_id(_id)
        if not car:
            return {'Mensagem': 'Carro não encontrado.'}, 404

        car.delete_from_db()
        return {'Mensagem': 'Carro excluído com sucesso.'}, 200


class CarRental(Resource):
    @fresh_jwt_required
    def patch(self, car_id, user_id):
        car = CarModel.find_by_id(car_id)
        if not car:
            return {'Mensagem': 'Carro não cadastrado.'}, 404

        if car.status == 'Indisponível':
            return {'Mensagem': 'Carro indisponível para retirada.'}, 400
        else:
            car.status = 'Indisponível'
            car.renter = user_id

        car.save_to_db()
        return car.json(), 200


class CarReturn(Resource):
    @fresh_jwt_required
    def patch(self, car_id):
        car = CarModel.find_by_id(car_id)
        if not car:
            return {'Mensagem': 'Carro não cadastrado.'}, 404

        if car.status == 'Disponível':
            return {'Mensagem': 'Carro indisponível para retorno.'}, 400
        else:
            car.status = 'Disponível'
            car.renter = None

        car.save_to_db()
        return car.json(), 200
