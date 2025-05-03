from gelir.ekle import gelir_ekle
from gelir.sil_guncelle import gelir_sil, gelir_guncelle

def menu_goster():
    print("\n--- Gelir İşlemleri ---")
    print("1. Gelir Ekle")
    print("2. Gelir Sil")
    print("3. Gelir Güncelle")
    print("0. Çıkış")

def main():
    while True:
        menu_goster()
        secim = input("Seçiminiz: ")

        if secim == "1":
            try:
                miktar = float(input("Gelir miktarı: "))
                kategori = input("Kategori: ")
                tarih = input("Tarih (YYYY-MM-DD, boşsa bugünün tarihi): ") or None
                gelir_ekle(miktar, kategori, tarih)
            except ValueError:
                print("Geçersiz miktar girdiniz.")
        
        elif secim == "2":
            try:
                gelir_id = int(input("Silinecek gelir ID'si: "))
                gelir_sil(gelir_id)
            except ValueError:
                print("Geçersiz ID.")

        elif secim == "3":
            try:
                gelir_id = int(input("Güncellenecek gelir ID'si: "))
                miktar = input("Yeni miktar (boşsa değişmez): ")
                kategori = input("Yeni kategori (boşsa değişmez): ")
                tarih = input("Yeni tarih (YYYY-MM-DD, boşsa değişmez): ")

                gelir_guncelle(
                    gelir_id,
                    float(miktar) if miktar else None,
                    kategori if kategori else None,
                    tarih if tarih else None
                )
            except ValueError:
                print("Girişlerde hata var, lütfen tekrar deneyin.")

        elif secim == "0":
            print("Çıkılıyor...")
            break
        else:
            print("Geçersiz seçim, tekrar deneyin.")

if __name__ == "__main__":
    main()
