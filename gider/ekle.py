from veritabani.baglanti import veritabani_baglan
from datetime import date

def gider_ekle(miktar, kategori, aciklama=None, tarih=None):
    con = veritabani_baglan()
    if con is None:
        return False

    cursor = con.cursor()

    try:
        if not tarih:
            tarih = date.today().isoformat()

        cursor.execute("""
            INSERT INTO gider (miktar, kategori, aciklama, tarih)
            VALUES (%s, %s, %s, %s)
        """, (miktar, kategori, aciklama, tarih))

        con.commit()
        print("Gider başarıyla eklendi.")
        return True
    except Exception as e:
        print(f"Gider ekleme hatası: {e}")
        return False
    finally:
        cursor.close()
        con.close()

if __name__ == "__main__":
    try:
        miktar = float(input("Gider miktarını giriniz: "))
        kategori = input("Gider kategorisini giriniz: ")
        aciklama = input("Açıklama (opsiyonel): ") or None
        tarih = input("Tarih (YYYY-MM-DD, boşsa bugünün tarihi): ") or None
        gider_ekle(miktar, kategori, aciklama, tarih)
    except ValueError:
        print("Geçerli bir miktar giriniz.")