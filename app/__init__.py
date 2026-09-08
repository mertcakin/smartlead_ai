from flask import Flask
from flask_cors import CORS

from config import Config
from .database import init_db
from .routes import main_bp, api_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(
        app,
        origins=Config.CORS_ORIGINS
    )

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