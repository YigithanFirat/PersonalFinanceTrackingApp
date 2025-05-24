from veritabani.baglanti import veritabani_baglan

def giderleri_listele():
    con = veritabani_baglan()
    if con is None:
        return {"success": False, "message": "Veritabanı bağlantısı başarısız.", "veriler": []}

    cursor = con.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM gider ORDER BY tarih DESC")
        kayitlar = cursor.fetchall()

        if not kayitlar:
            return {"success": True, "message": "Kayıtlı gider bulunamadı.", "veriler": []}

        return {"success": True, "message": "Giderler başarıyla listelendi.", "veriler": kayitlar}
    except Exception as e:
        return {"success": False, "message": f"Gider listeleme hatası: {e}", "veriler": []}
    finally:
        cursor.close()
        con.close()