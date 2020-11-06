from flask_restful import reqparse, Resource
from models.carBrand import CarBrand

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('brand',
                          type=str,
                          required=True,
                          help='Este campo deve ser preenchido'
                          )


class BrandRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        brand = CarBrand(**data)
        brand.save_to_db()
        return brand.json()


class BrandResource(Resource):
    def get(self, _id):
        brand = CarBrand.find_by_id(_id)

        if not brand:
            return {'Mensagem': 'Marca não encontrada.'}, 404

        return brand.json()

    def delete(self, _id):
        brand = CarBrand.find_by_id(_id)

        if not brand:
            return {'Mensagem': 'Marca não encontrada.'}, 404

        brand.delete_from_db()
        return {'Mensagem': 'Marca excluída com sucesso.'}, 200


class BrandList(Resource):
    def get(self):
        return {'brands': [brand.json() for brand in CarBrand.find_all()]}
