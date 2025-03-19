from http import HTTPStatus

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.models.product import ProductCreate, ProductResponse
from app.routes.errors import generic_error, validation_error
from app.services.product_service import ProductService
from app.utilities import cache
from app.utilities.cache import Entry

api_v1_blueprint = Blueprint('api/v1', __name__)
MAX_QUERY_RESULTS: int = 100

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
def get_product(product_id: int):
    cache_key = f"products:{product_id}"
    try:
        cached = cache.get(cache_key)
        if cached:
            product = cached
        else:
            product = ProductService.get_product(product_id)
            cache.set(cache_key, Entry(product))

        return jsonify(ProductResponse(**product).model_dump()), HTTPStatus.OK
    except ValidationError as e:
        return validation_error(e)
    except Exception as e:
        return generic_error()


@api_v1_blueprint.route('/products', methods=['GET'])
def get_all_products():
    limit = request.args.get('limit', default=50, type=int)
    offset = request.args.get('offset', default=0, type=int)
    cache_key = f"products:l{limit}:o{offset}"

    if limit > MAX_QUERY_RESULTS: limit = MAX_QUERY_RESULTS
    try:
        cached = cache.get(cache_key)
        if cached:
            products = cached
        else:
            products = ProductService.get_all_products(limit, offset)
            cache.set(cache_key, Entry(products))
        return (
            jsonify({
                "limit": limit,
                "offset": offset,
                "data": [ProductResponse(**product).model_dump() for product in products]
            }),
            HTTPStatus.OK
        )
    except ValidationError as e:
        return validation_error(e)
    except Exception as e:
        return generic_error()


@api_v1_blueprint.route('/products/<int:product_id>', methods=['PUT'])
def full_update_product(product_id: int):
    try:
        product_update = ProductCreate(**request.get_json())
        product = ProductService.full_update_product(
            product_id, product_update)
        return jsonify(ProductResponse(**product).model_dump()), HTTPStatus.OK
    except ValidationError as e:
        print(e)
        return validation_error(e)
    except Exception as e:
        print(e)
        return generic_error()
