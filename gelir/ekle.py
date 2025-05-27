from flask import request, jsonify, session
import datetime
from veritabani.baglanti import veritabani_baglan

def gelir_ekle():
    # Session'dan user_id alınır
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Giriş yapılmamış'}), 401

    conn = veritabani_baglan()
    cursor = conn.cursor()

    try:
        # Kullanıcının login durumu DB'den kontrol edilir
        cursor.execute("SELECT login FROM kullanicilar WHERE id = %s", (user_id,))
        result = cursor.fetchone()

        if not result or result[0] != 1:
            return jsonify({'success': False, 'message': 'Giriş yapılmamış'}), 401

        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Geçersiz JSON'}), 400

        miktar = data.get('miktar')
        kategori = data.get('kategori')
        tarih = data.get('tarih')

        if not all([miktar, kategori, tarih]):
            return jsonify({'success': False, 'message': 'Eksik veri var'}), 400

        try:
            tarih_obj = datetime.datetime.strptime(tarih, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'success': False, 'message': 'Tarih formatı geçersiz'}), 400

        cursor.execute("""
            INSERT INTO gelir (miktar, kategori, tarih, kullanici_id)
            VALUES (%s, %s, %s, %s)
        """, (miktar, kategori, tarih_obj, user_id))
        conn.commit()

    except Exception as e:
        print("DB Hatası:", e)
        return jsonify({'success': False, 'message': 'Sunucu hatası'}), 500

    finally:
        cursor.close()
        conn.close()

    return jsonify({'success': True, 'message': 'Gelir eklendi'}), 200