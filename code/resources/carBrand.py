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
    def get(self):
        pass

    def delete(self):
        pass


class BrandList(Resource):
    def get(self):
        pass
