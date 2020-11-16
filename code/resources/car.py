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
        return{'Mensagem': 'Carro excluído com sucesso.'}, 200


class CarList(Resource):
    @jwt_required
    def get(self):
        return {'cars': [car.json() for car in CarModel.find_all()]}, 200
