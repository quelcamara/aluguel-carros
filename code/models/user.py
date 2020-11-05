from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

    user_type = db.Column(db.Integer, db.ForeignKey('user_type.id'))
    credentials = db.relationship('UserType')

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
    def find_all(cls):
        return cls.query.all()


class UserType(db.Model):
    __tablename__ = 'user_type'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50))

    users = db.relationship('UserModel')

    def __init__(self, _id, description):
        self.id = _id
        self.description = description

    @staticmethod
    def employee():
        if not UserType.find_by_id(1):
            employee = UserType(1, 'Funcionário')
            employee.save_to_db()

    @staticmethod
    def client():
        if not UserType.find_by_id(2):
            client = UserType(2, 'Cliente')
            client.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
