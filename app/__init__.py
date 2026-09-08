from flask import Flask
from flask_cors import CORS

from config import Config
from .database import init_db
from .routes import main_bp, api_bp


def create_app():
    # Flask uygulamasını oluşturdum.
    app = Flask(__name__)

    # Uygulamanın ayarlarını Config sınıfından aldım.
    app.config.from_object(Config)

    # Wix üzerinden gelen API isteklerine izin verecek CORS ayarını yaptım.
    CORS(
        app,
        origins=Config.CORS_ORIGINS
    )

    # Uygulama başlarken veritabanını hazırladım.
    init_db(app)

    # Ana sayfa ve API yönlendirmelerini uygulamaya bağladım.
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    @app.route("/health")
    def health():
        # Sunucunun çalışıp çalışmadığını kontrol etmek için sağlık endpoint'i oluşturdum.
        return {
            "basari": True,
            "mesaj": "SmartLead AI çalışıyor."
        }, 200

    return app