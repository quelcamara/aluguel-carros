from flask_restful_swagger import swagger


@swagger.model
class UserModel:
    """Modelo de Objeto 'User'"""
    def __init__(self, username, password, name, user_type):
        self.username = username
        self.password = password
        self.name = name
        self.user_type = user_type


@swagger.model
class UsersLogin:
    def __init__(self, username, password):
        self.username = username
        self.password = password
