from veritabani.baglanti import veritabani_baglan
from datetime import datetime

def gelir_ekle(miktar, kategori, tarih=None):
    con = veritabani_baglan()
    if con is None:
        return False

    cursor = con.cursor()

    try:
        if not tarih:
            tarih = datetime.now().strftime('%Y-%m-%d')

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
    try:
        miktar = float(input("Gelir miktarını giriniz: "))
        kategori = input("Gelir kategorisini giriniz: ")
        gelir_ekle(miktar, kategori)
    except ValueError:
        print("Geçerli bir miktar giriniz.")