from veritabani.baglanti import veritabani_baglan

def gider_sil(gider_id):
    con = veritabani_baglan()
    if con is None:
        print("Veritabanı bağlantısı başarısız.")
        return False

    cursor = con.cursor()

    try:
        cursor.execute("DELETE FROM gider WHERE id = %s", (gider_id,))
        con.commit()
        print(f"{gider_id} numaralı gider başarıyla silindi.")
        return True
    except Exception as e:
        print(f"Gider silme hatası: {e}")
        return False
    finally:
        cursor.close()
        con.close()

def gider_guncelle(gider_id, miktar=None, kategori=None, aciklama=None, tarih=None):
    con = veritabani_baglan()
    if con is None:
        print("Veritabanı bağlantısı başarısız.")
        return False

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

        update_query = update_query.rstrip(', ')
        update_query += " WHERE id = %s"
        params.append(gider_id)
        cursor.execute(update_query, tuple(params))
        con.commit()
        print(f"{gider_id} numaralı gider başarıyla güncellendi.")
        return True
    except Exception as e:
        print(f"Gider güncelleme hatası: {e}")
        return False
    finally:
        cursor.close()
        con.close()