from flask_restful import Resource, reqparse
from flask_restful_swagger import swagger
from flask_jwt_extended import jwt_required, get_jwt_claims, fresh_jwt_required
from models.car import CarModel
from models.carBrand import CarBrand
from models.user import UserModel

_user_parse = reqparse.RequestParser()
_user_parse.add_argument('name',
                         type=str,
                         required=True,
                         nullable=False,
                         help='Este campo deve ser preenchido'
                         )
_user_parse.add_argument('color',
                         type=str,
                         default='-'
                         )
_user_parse.add_argument('year',
                         type=int,
                         required=True,
                         nullable=False,
                         help='Este campo deve ser preenchido'
                         )
_user_parse.add_argument('license_plate',
                         type=str,
                         required=True,
                         nullable=False,
                         help='Este campo deve ser preenchido'
                         )
_user_parse.add_argument('daily_cost',
                         type=float,
                         required=True,
                         nullable=False,
                         help='Este campo deve ser preenchido'
                         )
_user_parse.add_argument('brand_id',
                         type=int,
                         required=True,
                         nullable=False,
                         help='Este campo deve ser preenchido'
                         )
_user_parse.add_argument('status',
                         type=str,
                         default='Disponível',
                         nullable=False,
                         choices=('Disponível', 'Indisponível'),
                         help='Este campo deve ser preenchido com os valores: <Disponível> ou <Indisponível>'
                         )

_user_parse_query = reqparse.RequestParser()
_user_parse_query.add_argument('car-year',
                               dest='car_year',
                               required=False,
                               type=int,
                               location='args'
                               )
_user_parse_query.add_argument('car-brand',
                               dest='car_brand',
                               required=False,
                               type=int,
                               location='args'
                               )
_user_parse_query.add_argument('car-status',
                               dest='car_status',
                               required=False,
                               type=str,
                               choices=('disponivel', 'indisponivel'),
                               location='args'
                               )


class CarRegister(Resource):
    """Registro de veículos
        Cadastro de veículos no banco de dados.
        """
    @swagger.operation(
        summary="Registra um veículo no banco de dados.",
        notes="Para respostas válidas, todos os campos devem ser preenchidos. "
              "Para cadastrar um carro, é necessário que sua marca já tenha sido cadastrada, "
              "pois esses objetos carregar uma relação no banco de dados. Se excluído do corpo o campo 'status', "
              "será cadastrado um carro com status default 'disponível'. Esta é uma requisição permitida "
              "apenas para usuários do tipo 'funcionários'.",
        nickname="registroCarro",
        parameters=[
            {
                "name": "authorization",
                "in": "body",
                "description": "Autenticação de usuário.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Bearer {{access_token}}",
                "paramType": "header"
            },
            {
                "name": "body",
                "in": "body",
                "description": "Carro que precisa ser adicionado.",
                "required": True,
                "dataType": CarModel.__name__,
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "Created"
            },
            {
                "code": 400,
                "message": "Bad Request"
            },
            {
                "code": 401,
                "message": "Unauthorized"
            },
            {
                "code": 500,
                "message": "Internal Server Error"
            }
        ]
    )
    @jwt_required
    def post(self):
        claims = get_jwt_claims()

        if not claims['funcionario']:
            return {'Mensagem': 'Privilégio de administrador exigido.'}, 401

        data = _user_parse.parse_args()
        brand = CarBrand.find_by_id(data['brand_id'])
        if not brand:
            return {'Mensagem': 'Não foi possível registrar o carro, pois a marca inserida não está cadastrada.'}, 400

        car = CarModel(**data)
        try:
            car.save_to_db()
        except:
            return {'Mensagem': 'Um erro ocorreu ao tentar inserir o carro. Confira os dados de entrada.'}, 500

        return car.json(), 201


class CarList(Resource):
    """Lista de veículos
    Listagem de veículos cadastrados, sendo possível filtrar por ano, marca e status.
    """
    @swagger.operation(
        summary="Listagem de veículos do banco de dados.",
        notes="Se nenhum parâmetro for incluído, é retornada uma lista com todos os veículos. "
              "Caso contrário, retornará uma lista filtrada a partir dos parâmetros incluídos "
              "na requisição feita pelo usuário.",
        nickname="listaCarros",
        parameters=[
            {
                "name": "authorization",
                "in": "body",
                "description": "Autenticação de usuário.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Bearer {{access_token}}",
                "paramType": "header"
            },
            {
                "name": "car-year",
                "in": "query",
                "description": "Filtro para ano de veículos.",
                "required": False,
                "allowMultiple": False,
                "dataType": "Integer",
                "paramType": "query",
            },
            {
                "name": "car-brand",
                "in": "query",
                "description": "Filtro para marca de veículos.",
                "required": False,
                "allowMultiple": False,
                "dataType": "Integer",
                "paramType": "query"
            },
            {
                "name": "car-status",
                "in": "query",
                "description": "Filtro para status de veículos.",
                "required": False,
                "allowMultiple": False,
                "dataType": "",
                "paramType": "query",
                "enum": ["disponivel", "indisponivel"]
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
            {
                "code": 404,
                "message": "Not Found"
            },
        ]
    )
    @jwt_required
    def get(self):
        data = _user_parse_query.parse_args()
        car_list_filter = CarModel.filter(data['car_year'], data['car_brand'], data['car_status'])

        if car_list_filter == "no_year":
            return {'Mensagem': 'Não existem carros com este ano registrados.'}, 404
        elif car_list_filter == "no_brand":
            return {'Mensagem': 'Não existem carros registrados para esta marca.'}, 404
        elif car_list_filter == "no_status":
            return {'Mensagem': 'Não existem carros com este status no momento.'}, 404
        else:
            return {'cars:': [car.json() for car in car_list_filter]}, 200


class CarResource(Resource):
    """Recursos permitidos com veículos cadastrados
       Métodos para recuperar um veículo por ID e para excluir veículos do banco de dados.
       """
    @swagger.operation(
        summary="Encontra veículo por ID.",
        notes="Retorna um único veículo.",
        nickname="buscaCarroPorID",
        parameters=[
            {
                "name": "authorization",
                "in": "body",
                "description": "Autenticação de usuário.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Bearer {{access_token}}",
                "paramType": "header"
            },
            {
                "name": "_id",
                "in": "path",
                "description": "ID do veículo para ser retornado.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Integer",
                "paramType": "path"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
            {
                "code": 404,
                "message": "Not Found"
            },
        ]
    )
    @jwt_required
    def get(self, _id):
        car = CarModel.find_by_id(_id)

        if not car:
            return {'Mensagem': 'Carro não encontrado'}, 404
        return car.json(), 200

    @swagger.operation(
        summary="Exclui um veículo cadastrado.",
        notes="Para resposta válida, este endpoint deve ser testado com um fresh access token. "
              "Para isso, basta inserir o token gerado após realizado login. Token de acesso "
              "do tipo 'refresh' não é permitido para executar esta ação. Esta é "
              "uma requisição permitida apenas para usuários do tipo 'funcionários'.",
        nickname="excluiCarro",
        parameters=[
            {
                "name": "authorization",
                "in": "body",
                "description": "Autenticação de usuário.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Bearer {{access_token}}",
                "paramType": "header"
            },
            {
                "name": "_id",
                "in": "path",
                "description": "ID do veículo a ser excluído.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Integer",
                "paramType": "path"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
            {
                "code": 401,
                "message": "Unauthorized"
            },
            {
                "code": 404,
                "message": "Not Found"
            },
        ]
    )
    @fresh_jwt_required
    def delete(self, _id):
        claims = get_jwt_claims()
        if not claims['funcionario']:
            return {'Mensagem': 'Privilégio de administrador exigido.'}, 401

        car = CarModel.find_by_id(_id)
        if not car:
            return {'Mensagem': 'Carro não encontrado.'}, 404

        car.delete_from_db()
        return {'Mensagem': 'Carro excluído com sucesso.'}, 200


class CarRental(Resource):
    """Locação de veículos
    Registra, no banco de dados, a locação de um veículo.
    """
    @swagger.operation(
        summary="Aluga um veículo com status disponível.",
        notes="Para resposta válida, este endpoint deve ser testado com um fresh access token. "
              "Para isso, basta inserir o token gerado após realizado login. Token de acesso "
              "do tipo 'refresh' não é permitido para executar esta ação.",
        nickname="alugaCarro",
        parameters=[
            {
                "name": "authorization",
                "in": "body",
                "description": "Autenticação de usuário.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Bearer {{access_token}}",
                "paramType": "header"
            },
            {
                "name": "user_id",
                "in": "path",
                "description": "ID do usuário que irá retirar o carro.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Integer",
                "paramType": "path"
            },
            {
                "name": "car_id",
                "in": "path",
                "description": "ID do veículo a ser locado.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Integer",
                "paramType": "path"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
            {
                "code": 400,
                "message": "Bad Request"
            },
            {
                "code": 404,
                "message": "Not Found"
            },
        ]
    )
    @fresh_jwt_required
    def patch(self, car_id, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'Mensagem': 'Não foi possível completar a requisição, pois não há usuários cadastrados com este ID.'}, 400

        car = CarModel.find_by_id(car_id)
        if not car:
            return {'Mensagem': 'Carro não cadastrado.'}, 404

        if car.status == 'Indisponível':
            return {'Mensagem': 'Carro indisponível para retirada.'}, 400
        else:
            car.status = 'Indisponível'
            car.renter = user_id

        car.save_to_db()
        return car.json(), 200


class CarReturn(Resource):
    """Devolução de veículos
      Registra, no banco de dados, a devolução de um veículo.
      """
    @swagger.operation(
        summary="Retorna um veículo alugado.",
        notes="Para resposta válida, este endpoint deve ser testado com um fresh access token. "
              "Para isso, basta inserir o token gerado após realizado login. Token de acesso "
              "do tipo 'refresh' não é permitido para executar esta ação.",
        nickname="retornaCarro",
        parameters=[
            {
                "name": "authorization",
                "in": "body",
                "description": "Autenticação de usuário.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Bearer {{access_token}}",
                "paramType": "header"
            },
            {
                "name": "car_id",
                "in": "path",
                "description": "ID do veículo a ser devolvido.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Integer",
                "paramType": "path"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
            {
                "code": 400,
                "message": "Bad Request"
            },
            {
                "code": 404,
                "message": "Not Found"
            },
        ]
    )
    @fresh_jwt_required
    def patch(self, car_id):
        car = CarModel.find_by_id(car_id)
        if not car:
            return {'Mensagem': 'Carro não cadastrado.'}, 404

        if car.status == 'Disponível':
            return {'Mensagem': 'Carro indisponível para retorno.'}, 400
        else:
            car.status = 'Disponível'
            car.renter = None

        car.save_to_db()
        return car.json(), 200
