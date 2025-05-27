# gider/ekle.py

from flask import request, jsonify, session
from veritabani.baglanti import veritabani_baglan
from datetime import datetime

def gider_ekle():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Giriş yapmanız gerekiyor."}), 401

    try:
        data = request.get_json()
        miktar = float(data.get("miktar"))
        kategori = data.get("kategori")
        aciklama = data.get("aciklama", "")
        tarih_str = data.get("tarih")
        tarih = datetime.strptime(tarih_str, "%Y-%m-%d").date()
    except Exception as e:
        return jsonify({"success": False, "message": f"Geçersiz veri: {str(e)}"}), 400

    kullanici_id = session['user_id']

    con = veritabani_baglan()
    if not con:
        return jsonify({"success": False, "message": "Veritabanı bağlantısı başarısız"}), 500

    try:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO gider (miktar, kategori, aciklama, tarih, kullanici_id) VALUES (%s, %s, %s, %s, %s)",
            (miktar, kategori, aciklama, tarih, kullanici_id)
        )
        con.commit()
        cursor.close()
        con.close()
        return jsonify({"success": True, "message": "Gider eklendi."}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Veritabanı hatası: {str(e)}"}), 500