from datetime import datetime, timedelta
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.models.product import ProductCreate, ProductResponse
from app.models.sale import SalesTotalResponse, SalesTopProductsResponse
from app.routes.errors import date_range_error, generic_error, validation_error
from app.services.product_service import ProductService
from app.services.sale_service import SaleService
from app.utilities import cache
from app.utilities.cache import Entry

products_blueprint = Blueprint("products", __name__)
sales_blueprint = Blueprint("sales", __name__)
MAX_QUERY_RESULTS: int = 100


@products_blueprint.route("", methods=["POST"])
def create_product():
    try:
        product_data = ProductCreate(**request.get_json())
        new_product = ProductService.create_product(product_data)
        return jsonify(ProductResponse(**new_product).model_dump()), HTTPStatus.CREATED
    except ValidationError as e:
        return validation_error(e)
    except Exception as e:
        return generic_error()


@products_blueprint.route("/<int:product_id>", methods=["GET"])
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


@products_blueprint.route("", methods=["GET"])
def get_all_products():
    limit = request.args.get("limit", default=50, type=int)
    offset = request.args.get("offset", default=0, type=int)
    cache_key = f"products:l{limit}:o{offset}"

    if limit > MAX_QUERY_RESULTS:
        limit = MAX_QUERY_RESULTS
    try:
        cached = cache.get(cache_key)
        if cached:
            products = cached
        else:
            products = ProductService.get_all_products(limit, offset)
            cache.set(cache_key, Entry(products))
        return (
            jsonify(
                {
                    "limit": limit,
                    "offset": offset,
                    "data": [
                        ProductResponse(**product).model_dump() for product in products
                    ],
                }
            ),
            HTTPStatus.OK,
        )
    except ValidationError as e:
        return validation_error(e)
    except Exception as e:
        return generic_error()


@products_blueprint.route("<int:product_id>", methods=["PUT"])
def full_update_product(product_id: int):
    try:
        product_update = ProductCreate(**request.get_json())
        product = ProductService.full_update_product(product_id, product_update)
        return jsonify(ProductResponse(**product).model_dump()), HTTPStatus.OK
    except ValidationError as e:
        print(e)
        return validation_error(e)
    except Exception as e:
        print(e)
        return generic_error()


@sales_blueprint.route("total", methods=["GET"])
def get_total_sales():
    today = datetime.now().date()
    six_months_ago = today - timedelta(days=180)

    start_date = request.args.get("start_date", default=six_months_ago.isoformat(), type=str)
    end_date = request.args.get("end_date", default=today.isoformat(), type=str)

    if datetime.fromisoformat(start_date) > datetime.fromisoformat(end_date):
        return date_range_error(start_date, end_date)

    cache_key = f"totalsales:sd{start_date}:ed{end_date}"
    try:
        cached = cache.get(cache_key)
        if cached:
            total_result = cached
        else:
            total_result  = SaleService.get_total_for_period(start_date, end_date)
            cache.set(cache_key, Entry(total_result))
        return (
            jsonify(
                {
                    "start_date": start_date,
                    "end_date": end_date,
                    **SalesTotalResponse(**total_result).model_dump(),
                }
            ),
            HTTPStatus.OK,
        )
    except ValidationError as e:
        return validation_error(e)
    except Exception as e:
        return generic_error(e)


@sales_blueprint.route("top-products", methods=["GET"])
def get_top_n_products():
    today = datetime.now().date()
    six_months_ago = today - timedelta(days=180)

    start_date = request.args.get("start_date", default=six_months_ago.isoformat(), type=str)
    end_date = request.args.get("end_date", default=today.isoformat(), type=str)
    limit = request.args.get("limit", default=10, type=int)

    if datetime.fromisoformat(start_date) > datetime.fromisoformat(end_date):
        return date_range_error(start_date, end_date)

    cache_key = f"topnproducts:sd{start_date}:ed{end_date}:l{limit}"
    try:
        cached = cache.get(cache_key)
        if cached:
            total_result = cached
        else:
            total_result  = SaleService.get_n_top_products(start_date, end_date, limit)
            cache.set(cache_key, Entry(total_result))
        return (
            jsonify(
                {
                    "start_date": start_date,
                    "end_date": end_date,
                    "limit": limit,
                    "data": [
                        SalesTopProductsResponse(**result).model_dump()
                        for result in total_result
                    ]
                }
            ),
            HTTPStatus.OK,
        )
    except ValidationError as e:
        return validation_error(e)
    except Exception as e:
        return generic_error(e)
