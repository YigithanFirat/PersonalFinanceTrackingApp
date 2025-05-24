from veritabani.baglanti import veritabani_baglan
from datetime import date

def gider_ekle(miktar, kategori, aciklama=None, tarih=None):
    con = veritabani_baglan()
    if con is None:
        return {"success": False, "message": "Veritabanına bağlanılamadı."}

    cursor = con.cursor()

    try:
        if not tarih:
            tarih = date.today().isoformat()

        cursor.execute("""
            INSERT INTO gider (miktar, kategori, aciklama, tarih)
            VALUES (%s, %s, %s, %s)
        """, (miktar, kategori, aciklama, tarih))

        con.commit()
        return {"success": True, "message": "Gider başarıyla eklendi."}
    except Exception as e:
        return {"success": False, "message": f"Gider ekleme hatası: {e}"}
    finally:
        cursor.close()
        con.close()