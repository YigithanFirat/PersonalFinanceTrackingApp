import logging
from flask import request, jsonify, session
from datetime import datetime
from veritabani.baglanti import veritabani_baglan

logging.basicConfig(level=logging.DEBUG)

def gelir_ekle():
    if 'user_id' not in session:
        logging.debug("Oturum bulunamadı. Kullanıcı giriş yapmamış.")
        return jsonify({"success": False, "message": "Giriş yapmanız gerekiyor."}), 401

    data = request.get_json()
    if not data:
        logging.debug("JSON verisi alınamadı.")
        return jsonify({"success": False, "message": "Veri alınamadı."}), 400

    try:
        miktar = float(data.get("miktar", 0))
        kategori = data.get("kategori", "").strip()
        tarih_str = data.get("tarih", "").strip()

        if not miktar or not kategori or not tarih_str:
            logging.debug("Gerekli alanlar eksik: miktar/kategori/tarih.")
            return jsonify({"success": False, "message": "Miktar, kategori ve tarih zorunludur."}), 400

        tarih = datetime.strptime(tarih_str, "%Y-%m-%d").date()
    except (ValueError, TypeError) as e:
        logging.debug(f"Veri format hatası: {e}")
        return jsonify({"success": False, "message": "Geçersiz veri formatı."}), 400

    kullanici_id = session['user_id']
    logging.debug(f"Gelen veri: miktar={miktar}, kategori={kategori}, tarih={tarih}, kullanici_id={kullanici_id}")

    con = veritabani_baglan()
    if not con:
        logging.debug("Veritabanı bağlantısı sağlanamadı.")
        return jsonify({"success": False, "message": "Veritabanı bağlantısı başarısız."}), 500

    try:
        cursor = con.cursor()
        sql = """
            INSERT INTO gelir (miktar, kategori, tarih, kullanici_id)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (miktar, kategori, tarih, kullanici_id))
        con.commit()
        logging.debug("Gelir verisi başarıyla eklendi.")
    except Exception as e:
        logging.error(f"Veritabanı hatası: {e}")
        return jsonify({"success": False, "message": f"Veritabanı hatası: {str(e)}"}), 500
    finally:
        cursor.close()
        con.close()

    return jsonify({"success": True, "message": "Gelir başarıyla eklendi."})