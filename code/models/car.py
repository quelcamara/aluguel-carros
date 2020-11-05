from db import db
from flask_restful import reqparse
from models.carBrand import CarBrand

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


class CarModel(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    color = db.Column(db.String(50))
    year = db.Column(db.Integer)
    daily_cost = db.Column(db.Integer)

    brand_id = db.Column(db.Integer, db.ForeignKey('car_brands.id'))
    car_brand = db.relationship('CarBrand')

    def __init__(self, name, color, year, daily_cost):
        self.name = name
        self.color = color
        self.year = year
        self.daily_cost = daily_cost

