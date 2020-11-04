from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    name = db.Column(db.String(80))

    def __init__(self, username, password, name):
        self.username = username
        self.password = password
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()
