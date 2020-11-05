from db import db


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


class CarBrand(db.Model):
    __tablename__ = 'car_brands'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50))

    car_model = db.relationship('CarModel')

    def __init__(self, _id, brand):
        self.id = _id
        self.brand = brand
