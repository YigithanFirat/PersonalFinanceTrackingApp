from ..veritabani.baglanti import veritabani_baglan

def gelir_ekle(miktar, kategori, tarih=None):
    con = veritabani_baglan()
    if con is None:
        return False
    
    cursor = con.cursor()

    try:
        if not tarih:
            tarih = "CURRENT DATE"

        # Gelir verisini ekle
        cursor.execute("""
            INSERT INTO gelir (miktar, kategori, tarih) 
            VALUES (%s, %s, %s)
        """, (miktar, kategori, tarih))

        con.commit()
        print("Gelir başarıyla eklendi.")
        return True
    except Exception as e:
        print(f"Gelir ekleme hatası: {e}")
        return False
    finally:
        cursor.close()
        con.close()

if __name__ == "__main__":
    miktar = int(input("Gelir miktarını giriniz: "))
    kategori = "Maaş"
    gelir_ekle(miktar, kategori)