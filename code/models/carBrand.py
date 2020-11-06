from db import db


class CarBrand(db.Model):
    __tablename__ = 'car_brands'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50))

    car_model = db.relationship('CarModel')

    def __init__(self, brand):
        self.brand = brand

    def json(self):
        return {
            "id": self.id,
            "brand": self.brand
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