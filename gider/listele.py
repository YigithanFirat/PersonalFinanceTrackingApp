from veritabani.baglanti import veritabani_baglan

def giderleri_listele():
    con = veritabani_baglan()
    if con is None:
        print("Veritabanı bağlantısı başarısız.")
        return

    cursor = con.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM gider ORDER BY tarih DESC")
        kayitlar = cursor.fetchall()

        if not kayitlar:
            print("Kayıtlı gider bulunamadı.")
            return

        print("\n--- Gider Kayıtları ---")
        for gider in kayitlar:
            print(f"ID: {gider['id']}, Miktar: {gider['miktar']}, Kategori: {gider['kategori']}, "
                  f"Açıklama: {gider['aciklama']}, Tarih: {gider['tarih']}")
    except Exception as e:
        print(f"Gider listeleme hatası: {e}")
    finally:
        cursor.close()
        con.close()