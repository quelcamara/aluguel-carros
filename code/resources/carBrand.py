from flask_restful import reqparse, Resource
from flask_restful_swagger import swagger
from models.carBrand import CarBrand
from flask_jwt_extended import jwt_required, get_jwt_claims, fresh_jwt_required
from sqlalchemy import exc

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('brand',
                          type=str,
                          required=True,
                          nullable=False,
                          help='Este campo deve ser preenchido'
                          )


class BrandRegister(Resource):
    """Registro de marcas
    Cadastro de marcas de carros no banco de dados.
    """
    @swagger.operation(
        summary="Registra uma marca no banco de dados.",
        notes="Para respostas válidas, todos os campos devem ser preenchidos. Não é permitido "
              "o registro duplicado de marcas. Esta é uma requisição permitida "
              "apenas para usuários do tipo 'funcionários'.",
        nickname="registroMarca",
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
                "description": "Marca que precisa ser adicionada.",
                "required": True,
                "dataType": CarBrand.__name__,
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
            }
        ]
    )
    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        if not claims['funcionario']:
            return {'Mensagem': 'Privilégio de administrador exigido.'}, 401

        data = _user_parser.parse_args()
        if CarBrand.find_by_brand(data['brand']):
            return {'Mensagem': 'Marca de carro já cadastrada.'}, 400

        brand = CarBrand(**data)
        brand.save_to_db()
        return brand.json(), 201


class BrandList(Resource):
    """Lista de marcas de veículos
    Listagem de marcas cadastrados.
    """
    @swagger.operation(
        summary="Listagem de marcas do banco de dados.",
        notes="Retorna uma lista com as marcas de veículos cadastradas no banco de dados.",
        nickname="listaMarcas",
        parameters=[
            {
                "name": "authorization",
                "in": "body",
                "description": "Autenticação de usuário.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Bearer {{access_token}}",
                "paramType": "header"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            }
        ]
    )
    @jwt_required
    def get(self):
        return {'brands': [brand.json() for brand in CarBrand.find_all()]}, 200


class BrandResource(Resource):
    """Recursos permitidos com marcas cadastradas
       Métodos para recuperar uma marca por ID e para excluir marcas do banco de dados.
       """
    @swagger.operation(
        summary="Encontra marca por ID.",
        notes="Retorna uma única marca.",
        nickname="buscaMarcaPorID",
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
                "description": "ID da marca para ser retornada.",
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
    @jwt_required
    def get(self, _id):
        brand = CarBrand.find_by_id(_id)

        if not brand:
            return {'Mensagem': 'Marca não encontrada.'}, 404
        return brand.json(), 200

    @swagger.operation(
        summary="Exclui uma marca cadastrada.",
        notes="Para resposta válida, este endpoint deve ser testado com um fresh access token. "
              "Para isso, basta inserir o token gerado após realizado login. Token de acesso "
              "do tipo 'refresh' não é permitido para executar esta ação. Esta é "
              "uma requisição permitida apenas para usuários do tipo 'funcionários'.",
        nickname="excluiMarca",
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
                "description": "ID da marca cadastrada a ser excluída.",
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

        brand = CarBrand.find_by_id(_id)
        if not brand:
            return {'Mensagem': 'Marca não encontrada.'}, 404
        try:
            brand.delete_from_db()
        except exc.IntegrityError:
            return {'Mensagem': 'Não é possível excluir esta marca pois existem carros associados a ela.'}, 400

        return {'Mensagem': 'Marca excluída com sucesso.'}, 200
