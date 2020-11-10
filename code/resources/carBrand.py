from flask_restful import reqparse, Resource
from models.carBrand import CarBrand
from flask_jwt_extended import jwt_required, get_jwt_claims, fresh_jwt_required

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('brand',
                          type=str,
                          required=True,
                          nullable=False,
                          help='Este campo deve ser preenchido'
                          )


class BrandRegister(Resource):
    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        if not claims['funcionario']:
            return {'Mensagem': 'Privilégio de administrador exigido.'}, 401

        data = _user_parser.parse_args()
        if CarBrand.find_by_brand(data['brand']):
            return {'Mensagem': 'Marca de carro já cadastrada.'}, 400

        brand = CarBrand(**data)
        brand.save_to_db()
        return brand.json()


class BrandResource(Resource):
    @jwt_required
    def get(self, _id):
        brand = CarBrand.find_by_id(_id)

        if not brand:
            return {'Mensagem': 'Marca não encontrada.'}, 404

        return brand.json()

    @fresh_jwt_required
    def delete(self, _id):
        claims = get_jwt_claims()
        if not claims['funcionario']:
            return {'Mensagem': 'Privilégio de administrador exigido.'}, 401

        brand = CarBrand.find_by_id(_id)

        if not brand:
            return {'Mensagem': 'Marca não encontrada.'}, 404

        brand.delete_from_db()
        return {'Mensagem': 'Marca excluída com sucesso.'}, 200


class BrandList(Resource):
    @jwt_required
    def get(self):
        return {'brands': [brand.json() for brand in CarBrand.find_all()]}, 200
