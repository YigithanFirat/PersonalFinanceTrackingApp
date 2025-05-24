from veritabani.baglanti import veritabani_baglan

def gelirleri_listele():
    con = veritabani_baglan()
    if con is None:
        return {"success": False, "message": "Veritabanına bağlanılamadı.", "data": []}

    cursor = con.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM gelir ORDER BY tarih DESC")
        gelir_kayitlari = cursor.fetchall()

        return {
            "success": True,
            "message": f"{len(gelir_kayitlari)} kayıt bulundu." if gelir_kayitlari else "Hiç kayıt yok.",
            "data": gelir_kayitlari
        }

    except Exception as e:
        return {"success": False, "message": f"Gelirleri listelerken hata oluştu: {e}", "data": []}
    finally:
        cursor.close()
        con.close()