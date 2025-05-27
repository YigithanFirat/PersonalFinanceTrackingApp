from veritabani.baglanti import veritabani_baglan
from flask import Flask, request, jsonify, render_template
from datetime import datetime

def gider_sil(id):
    con = veritabani_baglan()
    if not con:
        return jsonify({"success": False, "message": "Veritabanı bağlantısı başarısız"})
    cursor = con.cursor()
    cursor.execute("DELETE FROM gider WHERE id=%s", (id,))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({"success": True, "message": "Gider silindi."})

def gider_guncelle(id):
    data = request.json
    try:
        miktar = float(data.get("miktar"))
        kategori = data.get("kategori")
        aciklama = data.get("aciklama", "")
        tarih_str = data.get("tarih")
        tarih = datetime.strptime(tarih_str, "%Y-%m-%d").date()
    except Exception:
        return jsonify({"success": False, "message": "Geçersiz veri"})

    con = veritabani_baglan()
    if not con:
        return jsonify({"success": False, "message": "Veritabanı bağlantısı başarısız"})
    cursor = con.cursor()
    cursor.execute("UPDATE gider SET miktar=%s, kategori=%s, aciklama=%s, tarih=%s WHERE id=%s", (miktar, kategori, aciklama, tarih, id))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({"success": True, "message": "Gider güncellendi."})