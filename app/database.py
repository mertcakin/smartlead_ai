import sqlite3
from flask import g
from config import Config


# Veritabanı bağlantısını oluşturdum ve tekrar kullanılmasını sağladım.
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("smartlead.db")
        g.db.row_factory = sqlite3.Row

    return g.db


# Lead ve giriş kayıtlarının tutulacağı tabloları oluşturdum.
def init_db(app):
    with app.app_context():
        db = get_db()

        # Lead kayıtlarının tutulacağı tabloyu oluşturdum.
        db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Yönetim paneli girişlerinin tutulacağı tabloyu oluşturdum.
        db.execute("""
            CREATE TABLE IF NOT EXISTS login_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_adi TEXT NOT NULL,
                durum TEXT NOT NULL,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        db.commit()


# Yeni müşteri bilgilerini veritabanına kaydetmek için bu fonksiyonu oluşturdum.
def lead_ekle(isim, telefon, mesaj):
    db = get_db()

    # Verileri parametre olarak göndererek SQL sorgusunu daha güvenli hale getirdim.
    db.execute(
        """
        INSERT INTO leads (isim, telefon, mesaj)
        VALUES (?, ?, ?)
        """,
        (isim, telefon, mesaj)
    )

    db.commit()


# Kayıtlı lead bilgilerini en yeniden eskiye doğru getirdim.
def tum_leadler():
    db = get_db()

    rows = db.execute(
        """
        SELECT id, isim, telefon, mesaj, tarih
        FROM leads
        ORDER BY tarih DESC
        """
    ).fetchall()

    return rows


# Yönetim paneli girişini kayıt altına almak için bu fonksiyonu oluşturdum.
def login_kaydi_ekle(kullanici_adi, durum):
    db = get_db()

    # Kullanıcı adı ve giriş durumunu veritabanına kaydettim.
    db.execute(
        """
        INSERT INTO login_logs (kullanici_adi, durum)
        VALUES (?, ?)
        """,
        (kullanici_adi, durum)
    )

    db.commit()


# Yönetim paneli giriş kayıtlarını en yeniden eskiye doğru getirdim.
def tum_login_kayitlari():
    db = get_db()

    rows = db.execute(
        """
        SELECT id, kullanici_adi, durum, tarih
        FROM login_logs
        ORDER BY tarih DESC
        """
    ).fetchall()

    return rows