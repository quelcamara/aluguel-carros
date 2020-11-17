from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    user_type = db.Column(db.Integer, db.ForeignKey('user_type.id'), nullable=False)
    credentials = db.relationship('UserType')

    rental_car = db.relationship('CarModel')

    def __init__(self, username, password, name, user_type):
        self.username = username
        self.password = password
        self.name = name
        self.user_type = user_type

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'type': self.user_type
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
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_type(cls, user_type):
        return cls.query.filter_by(user_type=user_type).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()
