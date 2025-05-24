from veritabani.baglanti import veritabani_baglan
from datetime import datetime

def gelir_ekle(miktar, kategori, tarih=None):
    con = veritabani_baglan()
    if con is None:
        return {"success": False, "message": "Veritabanı bağlantısı başarısız."}

    cursor = con.cursor()

    try:
        if not tarih:
            tarih = datetime.now().strftime('%Y-%m-%d')

        cursor.execute("""
            INSERT INTO gelir (miktar, kategori, tarih) 
            VALUES (%s, %s, %s)
        """, (miktar, kategori, tarih))

        con.commit()
        return {"success": True, "message": "Gelir başarıyla eklendi."}
    except Exception as e:
        return {"success": False, "message": f"Gelir ekleme hatası: {e}"}
    finally:
        cursor.close()
        con.close()