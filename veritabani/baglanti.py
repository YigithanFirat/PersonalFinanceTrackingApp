import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "[priadon1.5]",
    "database": "finans_db"
}

def veritabani_baglan():
    try:
        con = mysql.connector.connect(**DB_CONFIG)
        if con.is_connected():
            return con
    except Error as e:
        print(f"Veritabanı bağlantı hatası: {e}")
    return None