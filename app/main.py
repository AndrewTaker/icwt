from flask import Flask

from app.routes.api import api_v1_blueprint

app = Flask(__name__)
app.config.from_object('app.config.Config')
app.register_blueprint(api_v1_blueprint, url_prefix="/api/v1")

if __name__ == "__main__":
    app.run()
