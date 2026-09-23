from flask import Blueprint, render_template, request, jsonify
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from config import Config
from .database import lead_ekle, tum_leadler
from .services.ai_service import ai_service, AIServiceError


# Ana sayfa ve dashboard için yönlendirme yapısını oluşturdum.
main_bp = Blueprint("main", __name__)

# API işlemleri için ayrı bir yönlendirme yapısı oluşturdum.
api_bp = Blueprint("api", __name__, url_prefix="/api")


# Yönetim paneli girişinde kullanılacak güvenli token yapısını oluşturdum.
token_serializer = URLSafeTimedSerializer(Config.SECRET_KEY)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@api_bp.route("/login", methods=["POST"])
def login():
    # Wix'ten gelen kullanıcı adı ve şifre bilgilerini aldım.
    data = request.get_json()

    # Veri gönderilmemişse hata döndürdüm.
    if not data:
        return jsonify({
            "basari": False,
            "hata": "Giriş bilgileri gönderilmedi."
        }), 400

    kullanici_adi = data.get("kullanici_adi", "").strip().lower()
    sifre = data.get("sifre", "")

    # Kullanıcı adı veya şifre boşsa giriş işlemini durdurdum.
    if not kullanici_adi or not sifre:
        return jsonify({
            "basari": False,
            "hata": "Kullanıcı adı ve şifre zorunludur."
        }), 400

    # Render Environment Variables üzerinden kullanıcıyı kontrol ettim.
    dogru_sifre = Config.OGRETMENLER.get(kullanici_adi)

    if dogru_sifre and dogru_sifre == sifre:

        # Başarılı giriş için güvenli erişim token'ı oluşturdum.
        token = token_serializer.dumps({
            "kullanici_adi": kullanici_adi
        })

        return jsonify({
            "basari": True,
            "mesaj": "Giriş başarılı.",
            "token": token
        }), 200

    # Kullanıcı adı veya şifre yanlışsa girişe izin vermedim.
    return jsonify({
        "basari": False,
        "hata": "Kullanıcı adı veya şifre hatalı."
    }), 401


@api_bp.route("/sohbet", methods=["POST"])
def sohbet():
    # Kullanıcıdan gelen JSON verisini aldım.
    data = request.get_json()

    # Mesaj gönderilmemişse hata döndürdüm.
    if not data or not data.get("mesaj"):
        return jsonify({
            "basari": False,
            "hata": "Mesaj alanı zorunludur."
        }), 400

    mesaj = data.get("mesaj")
    gecmis = data.get("gecmis", [])

    try:
        # Kullanıcı mesajını AI servisine gönderip yanıtı aldım.
        cevap = ai_service.yanit_uret(mesaj, gecmis)

        return jsonify({
            "basari": True,
            "cevap": cevap
        }), 200

    except AIServiceError as e:
        # AI servisinde oluşan hatayı kullanıcıya JSON olarak döndürdüm.
        return jsonify({
            "basari": False,
            "hata": str(e)
        }), 503


@api_bp.route("/leads", methods=["POST"])
def lead_olustur():
    # Kullanıcıdan gelen lead bilgilerini aldım.
    data = request.get_json()

    # Veri gönderilmemişse hata döndürdüm.
    if not data:
        return jsonify({
            "basari": False,
            "hata": "Veri gönderilmedi."
        }), 400

    isim = data.get("isim")
    telefon = data.get("telefon")
    mesaj = data.get("mesaj", "")

    # İsim veya telefon eksikse kayıt oluşturmadım.
    if not isim or not telefon:
        return jsonify({
            "basari": False,
            "hata": "İsim ve telefon alanları zorunludur."
        }), 400

    # Lead bilgilerini veritabanına kaydettim.
    lead_ekle(isim, telefon, mesaj)

    return jsonify({
        "basari": True,
        "mesaj": "İletişim bilgileriniz başarıyla kaydedildi."
    }), 201


@api_bp.route("/leads", methods=["GET"])
def leadleri_getir():
    # Veritabanındaki tüm lead kayıtlarını aldım.
    leads = tum_leadler()

    lead_listesi = []

    # Veritabanı kayıtlarını API'nin döndüreceği formata dönüştürdüm.
    for lead in leads:
        lead_listesi.append({
            "id": lead["id"],
            "isim": lead["isim"],
            "telefon": lead["telefon"],
            "mesaj": lead["mesaj"],
            "tarih": lead["tarih"]
        })

    return jsonify({
        "basari": True,
        "leadler": lead_listesi
    }), 200