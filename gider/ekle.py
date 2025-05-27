from flask import request, jsonify, session
from veritabani.baglanti import veritabani_baglan
import datetime

def gider_ekle():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Giriş yapılmamış'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Geçersiz JSON'}), 400

    try:
        miktar = float(data.get('miktar'))
    except (TypeError, ValueError):
        return jsonify({'success': False, 'message': 'Miktar geçersiz'}), 400

    kategori = data.get('kategori')
    tarih = data.get('tarih')
    aciklama = data.get('aciklama', '')

    if not all([miktar, kategori, tarih]):
        return jsonify({'success': False, 'message': 'Eksik veri var'}), 400

    try:
        tarih_obj = datetime.datetime.strptime(tarih, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'success': False, 'message': 'Tarih formatı geçersiz'}), 400

    conn = None
    cursor = None
    try:
        conn = veritabani_baglan()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO gider (miktar, kategori, tarih, aciklama, kullanici_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (miktar, kategori, tarih_obj, aciklama, user_id))
        conn.commit()

    except Exception as e:
        print("Veritabanı hatası (gider_ekle):", e)
        return jsonify({'success': False, 'message': 'Veritabanı hatası'}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return jsonify({'success': True, 'message': 'Gider eklendi'}), 200