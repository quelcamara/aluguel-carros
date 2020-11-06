from db import db


class CarModel(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    color = db.Column(db.String(50))
    year = db.Column(db.Integer)
    daily_cost = db.Column(db.Float(precision=2))

    brand_id = db.Column(db.Integer, db.ForeignKey('car_brands.id'))
    car_brand = db.relationship('CarBrand')

    def __init__(self, name, color, year, daily_cost, brand_id):
        self.name = name
        self.color = color
        self.year = year
        self.daily_cost = daily_cost
        self.brand_id = brand_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'year': self.year,
            'daily_cost': self.daily_cost,
            'brand_id': self.brand_id
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
