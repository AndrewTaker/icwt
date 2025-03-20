from flask import Flask, Blueprint
from app.routes.api import products_blueprint, sales_blueprint

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    api_v1_blueprint = Blueprint("api_v1", __name__, url_prefix="/api/v1")
    api_v1_blueprint.register_blueprint(products_blueprint, url_prefix="/products")
    api_v1_blueprint.register_blueprint(sales_blueprint, url_prefix="/sales")
    app.register_blueprint(api_v1_blueprint)

    return app
