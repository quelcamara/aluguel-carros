from db import db


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
