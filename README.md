# RENVION SmartLead AI

RENVION SmartLead AI, ziyaretçilerin RENVION prototip hakkında yapay zekâ ile bilgi almasını ve iletişim bilgilerini bırakmasını sağlayan bir lead toplama sistemidir.

Sistem iki arayüzden oluşur:

- B2C: Ziyaretçinin yapay zekâ ile sohbet ettiği ve iletişim bilgilerini bıraktığı arayüz.
- B2B: Oluşturulan lead kayıtlarının görüntülendiği yönetim paneli.

## Kullanılan Teknolojiler

- Python
- Flask
- SQLite
- Groq API
- Wix Velo
- REST API
- GitHub
- Render

## Proje Yapısı

```text
smartlead_ai/
├── run.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── app/
    ├── __init__.py
    ├── database.py
    ├── routes.py
    ├── templates/
    │   ├── index.html
    │   └── dashboard.html
    └── services/
        ├── __init__.py
        └── ai_service.py
```

## Kurulum

Sanal ortam oluşturulur:

python -m venv venv

Sanal ortam aktive edilir:

venv\Scripts\activate

Bağımlılıklar yüklenir:

pip install -r requirements.txt

.env dosyasına gerekli API anahtarı eklenir:

GROQ_API_KEY=your_api_key
SECRET_KEY=your_secret_key

Uygulama çalıştırılır:

python run.py

## Kullanım

B2C arayüzü Wix Velo kullanılarak hazırlanmıştır. Kullanıcı RENVION prototip hakkında yapay zekâya soru sorabilir ve iletişim bilgilerini sisteme kaydedebilir.

B2B yönetim paneli üzerinden kaydedilen lead bilgileri görüntülenebilir.

Wix arayüzleri backend API üzerinden Render üzerinde çalışan Python Flask uygulamasına bağlanmaktadır.

## Canlı Sistem

Backend Render üzerinde yayınlanmıştır.

https://smartlead-ai-wcsw.onrender.com