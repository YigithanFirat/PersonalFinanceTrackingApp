from veritabani.baglanti import veritabani_baglan

def gider_sil(gider_id):
    con = veritabani_baglan()
    if con is None:
        return {"success": False, "message": "Veritabanı bağlantısı başarısız."}

    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM gider WHERE id = %s", (gider_id,))
        con.commit()
        if cursor.rowcount == 0:
            return {"success": False, "message": f"{gider_id} numaralı gider bulunamadı."}
        return {"success": True, "message": f"{gider_id} numaralı gider başarıyla silindi."}
    except Exception as e:
        return {"success": False, "message": f"Gider silme hatası: {e}"}
    finally:
        cursor.close()
        con.close()

def gider_guncelle(gider_id, miktar=None, kategori=None, aciklama=None, tarih=None):
    con = veritabani_baglan()
    if con is None:
        return {"success": False, "message": "Veritabanı bağlantısı başarısız."}

    cursor = con.cursor()
    try:
        update_query = "UPDATE gider SET "
        params = []

        if miktar is not None:
            update_query += "miktar = %s, "
            params.append(miktar)
        if kategori is not None:
            update_query += "kategori = %s, "
            params.append(kategori)
        if aciklama is not None:
            update_query += "aciklama = %s, "
            params.append(aciklama)
        if tarih is not None:
            update_query += "tarih = %s, "
            params.append(tarih)

        if not params:
            return {"success": False, "message": "Güncellenecek bir alan girilmedi."}

        update_query = update_query.rstrip(', ') + " WHERE id = %s"
        params.append(gider_id)

        cursor.execute(update_query, tuple(params))
        con.commit()

        if cursor.rowcount == 0:
            return {"success": False, "message": "Güncellenecek gider bulunamadı."}
        return {"success": True, "message": f"{gider_id} numaralı gider başarıyla güncellendi."}
    except Exception as e:
        return {"success": False, "message": f"Gider güncelleme hatası: {e}"}
    finally:
        cursor.close()
        con.close()