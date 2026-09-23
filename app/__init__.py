from flask import Flask, make_response
from flask_cors import CORS

from config import Config
from .database import init_db
from .routes import main_bp, api_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "*",
                "allow_headers": [
                    "Content-Type",
                    "Authorization"
                ],
                "methods": [
                    "GET",
                    "POST",
                    "OPTIONS"
                ]
            }
        }
    )

    # Wix'in gönderdiği OPTIONS (preflight) isteklerini karşıla
    @app.before_request
    def handle_preflight():
        from flask import request

        if request.method == "OPTIONS":
            response = make_response()
            response.status_code = 204
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            return response

    init_db(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    @app.route("/health")
    def health():
        return {
            "basari": True,
            "mesaj": "SmartLead AI çalışıyor."
        }, 200

    return app