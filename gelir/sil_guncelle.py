from veritabani.baglanti import veritabani_baglan

def gelir_sil(gelir_id):
    con = veritabani_baglan()
    if con is None:
        return {"success": False, "message": "Veritabanına bağlanılamadı."}

    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM gelir WHERE id = %s", (gelir_id,))
        con.commit()

        if cursor.rowcount == 0:
            return {"success": False, "message": "Belirtilen ID'ye ait gelir kaydı bulunamadı."}

        return {"success": True, "message": "Gelir başarıyla silindi."}
    except Exception as e:
        return {"success": False, "message": f"Silme hatası: {e}"}
    finally:
        cursor.close()
        con.close()

def gelir_guncelle(gelir_id, yeni_miktar=None, yeni_kategori=None, yeni_tarih=None):
    con = veritabani_baglan()
    if con is None:
        return {"success": False, "message": "Veritabanına bağlanılamadı."}

    cursor = con.cursor()
    try:
        sorgu = "UPDATE gelir SET "
        degerler = []

        if yeni_miktar is not None:
            sorgu += "miktar = %s, "
            degerler.append(yeni_miktar)
        if yeni_kategori is not None:
            sorgu += "kategori = %s, "
            degerler.append(yeni_kategori)
        if yeni_tarih is not None:
            sorgu += "tarih = %s, "
            degerler.append(yeni_tarih)

        if not degerler:
            return {"success": False, "message": "Güncellenecek bir alan girilmedi."}

        sorgu = sorgu.rstrip(", ") + " WHERE id = %s"
        degerler.append(gelir_id)

        cursor.execute(sorgu, tuple(degerler))
        con.commit()

        if cursor.rowcount == 0:
            return {"success": False, "message": "Güncellenecek kayıt bulunamadı."}

        return {"success": True, "message": "Gelir başarıyla güncellendi."}
    except Exception as e:
        return {"success": False, "message": f"Güncelleme hatası: {e}"}
    finally:
        cursor.close()
        con.close()