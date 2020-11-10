from db import db


class CarModel(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50))
    year = db.Column(db.Integer, nullable=False)
    license_plate = db.Column(db.String(50), nullable=False)
    daily_cost = db.Column(db.Float(precision=2), nullable=False)

    brand_id = db.Column(db.Integer, db.ForeignKey('car_brands.id'), nullable=False)
    car_brand = db.relationship('CarBrand')

    status = db.Column(db.String(50), nullable=False)
    renter = db.Column(db.Integer, db.ForeignKey('users.id'))
    renter_id = db.relationship('UserModel')

    def __init__(self, name, color, year, daily_cost, brand_id, license_plate, status):
        self.name = name
        self.color = color
        self.year = year
        self.license_plate = license_plate
        self.daily_cost = daily_cost
        self.brand_id = brand_id
        self.status = status

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'year': self.year,
            'license_plate': self.license_plate,
            'daily_cost': self.daily_cost,
            'brand_id': self.brand_id,
            'status': self.status
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
