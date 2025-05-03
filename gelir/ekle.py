from veritabani.baglanti import veritabani_baglan
from datetime import datetime

def gelir_ekle(miktar, kategori, tarih=None):
    """
    Gelir ekler.
    :param miktar: Gelir miktarı (decimal)
    :param kategori: Gelir kategorisi (string)
    :param tarih: Gelir tarihi (optional, None olarak verilirse CURRENT_DATE kullanılır)
    :return: Başarılıysa True, hata varsa False
    """
    con = veritabani_baglan()
    if con is None:
        return False

    cursor = con.cursor()

    try:
        # Eğer tarih belirtilmediyse, güncel tarihi kullan
        if not tarih:
            # Python'dan tarih al, 'YYYY-MM-DD' formatında
            tarih = datetime.now().strftime('%Y-%m-%d')

        # Gelir verisini ekle
        cursor.execute("""
            INSERT INTO gelir (miktar, kategori, tarih) 
            VALUES (%s, %s, %s)
        """, (miktar, kategori, tarih))

        con.commit()  # Değişiklikleri kaydet
        print("Gelir başarıyla eklendi.")
        return True
    except Exception as e:
        print(f"Gelir ekleme hatası: {e}")
        return False
    finally:
        cursor.close()
        con.close()

# Fonksiyonu test etmek için örnek:
if __name__ == "__main__":
    try:
        miktar = float(input("Gelir miktarını giriniz: "))  # Kullanıcıdan miktarı al
        kategori = input("Gelir kategorisini giriniz: ")  # Kullanıcıdan kategori al
        gelir_ekle(miktar, kategori)  # Gelir ekle fonksiyonunu çağır
    except ValueError:
        print("Geçerli bir miktar giriniz.")