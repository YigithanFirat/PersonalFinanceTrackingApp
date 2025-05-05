from gelir.ekle import gelir_ekle
from gelir.sil_guncelle import gelir_sil, gelir_guncelle
from gelir.listele import gelirleri_listele
from gider.ekle import gider_ekle
from gider.listele import giderleri_listele
from gider.sil_guncelle import gider_sil, gider_guncelle
from raporlar.grafik_olustur import gelir_grafik, gider_grafik, gelir_gider_karsilastir
from utils.tarih_formatla import tarih_formatla

# -----------------------------
# Menü Gösterim Fonksiyonları
# -----------------------------

def ana_menu_goster():
    print("\n--- Ana Menü ---")
    print("1. Gelir İşlemleri")
    print("2. Gider İşlemleri")
    print("3. Grafik Raporları")
    print("0. Çıkış")

def gelir_menu_goster():
    print("\n--- Gelir İşlemleri ---")
    print("1. Gelir Ekle")
    print("2. Gelir Sil")
    print("3. Gelir Güncelle")
    print("4. Gelirleri Listele")
    print("0. Geri Dön")

def gider_menu_goster():
    print("\n--- Gider İşlemleri ---")
    print("1. Gider Ekle")
    print("2. Gider Listele")
    print("3. Gider Sil")
    print("4. Gider Güncelle")
    print("0. Geri Dön")

def grafik_menu_goster():
    print("\n--- Grafik Raporları ---")
    print("1. Aylık Gelir Grafiği")
    print("2. Aylık Gider Grafiği")
    print("3. Aylık Gelir-Gider Karşılaştırması")
    print("0. Geri Dön")

# -----------------------------
# İşlem Fonksiyonları
# -----------------------------

def gelir_islemleri():
    while True:
        gelir_menu_goster()
        secim = input("Seçiminiz: ")

        if secim == "1":
            try:
                miktar = float(input("Gelir miktarı: "))
                kategori = input("Kategori: ")
                tarih = tarih_formatla(input("Tarih (YYYY-MM-DD, boşsa bugünün tarihi): "))
                if tarih:
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
                tarih_input = input("Yeni tarih (YYYY-MM-DD, boşsa değişmez): ")
                tarih = tarih_formatla(tarih_input) if tarih_input else None

                gelir_guncelle(
                    gelir_id,
                    float(miktar) if miktar else None,
                    kategori if kategori else None,
                    tarih
                )
            except ValueError:
                print("Girişlerde hata var, lütfen tekrar deneyin.")
        elif secim == "4":
            gelirleri_listele()
        elif secim == "0":
            break
        else:
            print("Geçersiz seçim.")

def gider_islemleri():
    while True:
        gider_menu_goster()
        secim = input("Seçiminiz: ")

        if secim == "1":
            try:
                miktar = float(input("Gider miktarı: "))
                kategori = input("Kategori: ")
                aciklama = input("Açıklama (opsiyonel): ")
                tarih = tarih_formatla(input("Tarih (YYYY-MM-DD, boşsa bugünün tarihi): "))
                if tarih:
                    gider_ekle(miktar, kategori, aciklama, tarih)
            except ValueError:
                print("Geçersiz miktar girdiniz.")
        elif secim == "2":
            giderleri_listele()
        elif secim == "3":
            try:
                gider_id = int(input("Silinecek gider ID'si: "))
                gider_sil(gider_id)
            except ValueError:
                print("Geçersiz ID.")
        elif secim == "4":
            try:
                gider_id = int(input("Güncellenecek gider ID'si: "))
                miktar = input("Yeni miktar (boşsa değişmez): ")
                kategori = input("Yeni kategori (boşsa değişmez): ")
                aciklama = input("Yeni açıklama (boşsa değişmez): ")
                tarih_input = input("Yeni tarih (YYYY-MM-DD, boşsa değişmez): ")
                tarih = tarih_formatla(tarih_input) if tarih_input else None

                gider_guncelle(
                    gider_id,
                    float(miktar) if miktar else None,
                    kategori if kategori else None,
                    aciklama if aciklama else None,
                    tarih
                )
            except ValueError:
                print("Geçersiz giriş.")
        elif secim == "0":
            break
        else:
            print("Geçersiz seçim.")

def grafik_raporlari():
    while True:
        grafik_menu_goster()
        secim = input("Seçiminiz: ")

        if secim == "1":
            gelir_grafik()
        elif secim == "2":
            gider_grafik()
        elif secim == "3":
            gelir_gider_karsilastir()
        elif secim == "0":
            break
        else:
            print("Geçersiz seçim.")

# -----------------------------
# Ana Fonksiyon
# -----------------------------

def main():
    while True:
        ana_menu_goster()
        secim = input("Seçiminiz: ")

        if secim == "1":
            gelir_islemleri()
        elif secim == "2":
            gider_islemleri()
        elif secim == "3":
            grafik_raporlari()
        elif secim == "0":
            print("Programdan çıkılıyor...")
            break
        else:
            print("Geçersiz seçim.")

if __name__ == "__main__":
    main()