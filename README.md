# RENVION SmartLead AI

RENVION SmartLead AI, ziyaretçilerin yapay zekâ ile RENVION prototip hakkında bilgi almasını ve iletişim bilgilerini bırakmasını sağlayan yapay zekâ destekli bir lead toplama sistemidir.

Sistem iki temel arayüzden oluşur:

- B2C Karşılama Sayfası: Ziyaretçi yapay zekâ ile sohbet eder ve iletişim bilgilerini bırakır.
- B2B Yönetim Paneli: İşletme sahibi oluşturulan lead kayıtlarını görüntüler.

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

## Sistem Mimarisi

Proje Separation of Concerns prensibine göre yapılandırılmıştır.

- config.py: Uygulama ayarlarını ve ortam değişkenlerini yönetir.
- database.py: SQLite veritabanı işlemlerini gerçekleştirir.
- ai_service.py: Yapay zekâ API çağrılarını gerçekleştirir.
- routes.py: HTTP isteklerini karşılar ve ilgili katmana yönlendirir.
- __init__.py: Flask uygulamasını oluşturur.
- run.py: Uygulamayı çalıştırır.

SQL işlemleri yalnızca database.py içerisinde gerçekleştirilir.
Yapay zekâ API çağrıları yalnızca ai_service.py içerisinde gerçekleştirilir.

## API Uç Noktaları

### GET /
B2C karşılama sayfasını açar.

### GET /dashboard
B2B yönetim panelini açar.

### POST /api/sohbet
Kullanıcının mesajını yapay zekâ servisine gönderir ve yanıtı döndürür.

Örnek istek:

{
    "mesaj": "RENVION prototip nedir?"
}

### POST /api/leads
Yeni bir lead kaydı oluşturur.

Örnek istek:

{
    "isim": "Mert Test",
    "telefon": "05550000000",
    "mesaj": "RENVION prototip hakkında bilgi almak istiyorum."
}

### GET /api/leads
Kayıtlı tüm leadleri en yeniden eskiye doğru getirir.

### GET /health
Backend servisinin çalışıp çalışmadığını kontrol eder.

## Güvenlik

- API anahtarları .env dosyasında tutulur.
- .env dosyası GitHub'a yüklenmez.
- SQL sorgularında parametreli sorgular (?) kullanılır.
- Dış servis çağrılarında try-except hata yönetimi uygulanır.
- API yanıtlarında JSON hata mesajları kullanılır.

## Kurulum

Projeyi klonladıktan sonra sanal ortam oluşturulur:

python -m venv venv

Sanal ortam aktive edilir ve bağımlılıklar yüklenir:

pip install -r requirements.txt

.env dosyası oluşturularak gerekli ortam değişkenleri eklenir.

Örnek:

GROQ_API_KEY=your_api_key
SECRET_KEY=your_secret_key

Uygulamayı çalıştırmak için:

python run.py

## Canlı Sistem

Backend Render üzerinde yayınlanmıştır.

Health kontrolü:

https://smartlead-ai-wcsw.onrender.com/health

Wix arayüzü backend API üzerinden bu servise bağlanmaktadır.

## Proje Amacı

Bu proje ile Flask tabanlı bir backend, SQLite veritabanı, yapay zekâ API entegrasyonu ve Wix Velo frontend bağlantısının modüler bir mimari içerisinde birlikte kullanılması amaçlanmıştır.