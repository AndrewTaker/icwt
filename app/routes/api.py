from flask import Blueprint, request, jsonify
from app.services.product_service import ProductService
from app.models.schemas import ProductCreate, ProductResponse
from app.routes.errors import handle_validation_error

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route("/kek", methods=['GET'])
def return_kek():
    return jsonify({"hi": "there"}), 200

@api_blueprint.route('/products', methods=['POST'])
def create_product():
    data = request.json
    product_data = ProductCreate(**data)
    new_product = ProductService.create_product(product_data)
    return jsonify(ProductResponse(**new_product).model_dump()), 201

@api_blueprint.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = ProductService.get_product(product_id)
        return jsonify(ProductResponse(**product).model_dump()), 200
    except Exception as e:
        return handle_validation_error(e)

@api_blueprint.route('/products', methods=['GET'])
def get_all_products():
    products = ProductService.get_all_products()
    return jsonify([ProductResponse(**product).model_dump() for product in products]), 200
