from veritabani.baglanti import veritabani_baglan
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # CORS açıldı

def gelir_guncelle(id):
    data = request.json
    try:
        miktar = float(data.get("miktar"))
        kategori = data.get("kategori")
        tarih_str = data.get("tarih")
        tarih = datetime.strptime(tarih_str, "%Y-%m-%d").date()
    except Exception:
        return jsonify({"success": False, "message": "Geçersiz veri"})

    con = veritabani_baglan()
    if not con:
        return jsonify({"success": False, "message": "Veritabanı bağlantısı başarısız"})
    cursor = con.cursor()
    cursor.execute("UPDATE gelir SET miktar=%s, kategori=%s, tarih=%s WHERE id=%s", (miktar, kategori, tarih, id))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({"success": True, "message": "Gelir güncellendi."})

def gelir_sil(id):
    con = veritabani_baglan()
    if not con:
        return jsonify({"success": False, "message": "Veritabanı bağlantısı başarısız"})
    cursor = con.cursor()
    cursor.execute("DELETE FROM gelir WHERE id=%s", (id,))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({"success": True, "message": "Gelir silindi."})