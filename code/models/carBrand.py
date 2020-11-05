from db import db
from flask_restful import reqparse

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('brand',
                          type=str,
                          required=True,
                          help='Este campo deve ser preenchido'
                          )


class CarBrand(db.Model):
    __tablename__ = 'car_brands'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50))

    car_model = db.relationship('CarModel')

    def __init__(self, _id, brand):
        self.id = _id
        self.brand = brand
