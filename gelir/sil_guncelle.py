from veritabani.baglanti import veritabani_baglan
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

def gelir_guncelle(id):
    data = request.json
    if not data:
        return jsonify({"success": False, "message": "İstek verisi eksik"}), 400

    try:
        miktar = float(data.get("miktar", 0))
        kategori = data.get("kategori", "").strip()
        tarih_str = data.get("tarih", "")
        tarih = datetime.strptime(tarih_str, "%Y-%m-%d").date()

        if not kategori:
            raise ValueError("Kategori boş olamaz")
    except (ValueError, TypeError) as e:
        return jsonify({"success": False, "message": f"Geçersiz veri: {str(e)}"}), 400

    con = veritabani_baglan()
    if not con:
        return jsonify({"success": False, "message": "Veritabanı bağlantısı başarısız"}), 500

    try:
        cursor = con.cursor()
        cursor.execute(
            "UPDATE gelir SET miktar=%s, kategori=%s, tarih=%s WHERE id=%s",
            (miktar, kategori, tarih, id)
        )
        con.commit()
        return jsonify({"success": True, "message": "Gelir güncellendi."})
    except Exception as e:
        return jsonify({"success": False, "message": f"Güncelleme hatası: {str(e)}"}), 500
    finally:
        cursor.close()
        con.close()

def gelir_sil(id):
    con = veritabani_baglan()
    if not con:
        return jsonify({"success": False, "message": "Veritabanı bağlantısı başarısız"}), 500

    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM gelir WHERE id=%s", (id,))
        con.commit()
        return jsonify({"success": True, "message": "Gelir silindi."})
    except Exception as e:
        return jsonify({"success": False, "message": f"Silme hatası: {str(e)}"}), 500
    finally:
        cursor.close()
        con.close()