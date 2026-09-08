import sqlite3
from flask import g
from config import Config


# Veritabanı bağlantısını oluşturdum ve tekrar kullanılmasını sağladım.
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("smartlead.db")
        g.db.row_factory = sqlite3.Row

    return g.db


# Lead kayıtlarının tutulacağı tabloyu oluşturdum.
def init_db(app):
    with app.app_context():
        db = get_db()

        db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
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