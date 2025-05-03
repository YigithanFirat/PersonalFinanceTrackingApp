from veritabani.baglanti import veritabani_baglan
from datetime import datetime

def gelir_sil(gelir_id):
    """Verilen ID'ye sahip gelir kaydını siler."""
    con = veritabani_baglan()
    if con is None:
        return False

    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM gelir WHERE id = %s", (gelir_id,))
        con.commit()
        if cursor.rowcount == 0:
            print("Belirtilen ID'ye ait gelir kaydı bulunamadı.")
            return False
        print("Gelir başarıyla silindi.")
        return True
    except Exception as e:
        print(f"Silme hatası: {e}")
        return False
    finally:
        cursor.close()
        con.close()

def gelir_guncelle(gelir_id, yeni_miktar=None, yeni_kategori=None, yeni_tarih=None):
    """Verilen ID'ye sahip gelir kaydını günceller."""
    con = veritabani_baglan()
    if con is None:
        return False

    cursor = con.cursor()
    try:
        # Güncellenecek alanları belirle
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
            print("Güncellenecek bir alan girilmedi.")
            return False

        # Sondaki virgülü kaldır
        sorgu = sorgu.rstrip(", ") + " WHERE id = %s"
        degerler.append(gelir_id)

        cursor.execute(sorgu, tuple(degerler))
        con.commit()

        if cursor.rowcount == 0:
            print("Güncellenecek kayıt bulunamadı.")
            return False
        print("Gelir başarıyla güncellendi.")
        return True
    except Exception as e:
        print(f"Güncelleme hatası: {e}")
        return False
    finally:
        cursor.close()
        con.close()

# Test / terminalden çalıştırma
if __name__ == "__main__":
    print("1 - Gelir Sil")
    print("2 - Gelir Güncelle")
    secim = input("İşlem seçiniz (1/2): ")

    try:
        if secim == "1":
            gelir_id = int(input("Silinecek gelir ID'sini giriniz: "))
            gelir_sil(gelir_id)
        elif secim == "2":
            gelir_id = int(input("Güncellenecek gelir ID'sini giriniz: "))
            miktar = input("Yeni miktar (boş bırakılırsa değişmez): ")
            kategori = input("Yeni kategori (boş bırakılırsa değişmez): ")
            tarih = input("Yeni tarih (YYYY-MM-DD, boşsa değişmez): ")

            # Boş bırakılanları None yap
            miktar = float(miktar) if miktar else None
            kategori = kategori if kategori else None
            tarih = tarih if tarih else None

            gelir_guncelle(gelir_id, miktar, kategori, tarih)
        else:
            print("Geçersiz seçim.")
    except ValueError:
        print("Geçersiz giriş.")