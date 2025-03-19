from http import HTTPStatus
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.services.product_service import ProductService
from app.models.schemas import ProductCreate, ProductResponse
from app.routes.errors import validation_error, generic_error
from app.utilities.cache import Cache

api_v1_blueprint = Blueprint('api/v1', __name__)

@api_v1_blueprint.route('/products', methods=['POST'])
def create_product():
    try:
        product_data = ProductCreate(**request.get_json())
        new_product = ProductService.create_product(product_data)
        return jsonify(ProductResponse(**new_product).model_dump()), HTTPStatus.CREATED
    except ValidationError as e:
        return validation_error(e)
    except Exception as e:
        return generic_error()

@api_v1_blueprint.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = ProductService.get_product(product_id)
        return jsonify(ProductResponse(**product).model_dump()), HTTPStatus.OK
    except ValidationError as e:
        return validation_error(e)
    except Exception as e:
        return generic_error()

@api_v1_blueprint.route('/products', methods=['GET'])
def get_all_products():
    try:
        products = ProductService.get_all_products()
        return (
                jsonify([ProductResponse(**product).model_dump() for product in products]),
                HTTPStatus.OK
        )
    except ValidationError as e:
        return validation_error(e)
    except Exception as e:
        return generic_error()
