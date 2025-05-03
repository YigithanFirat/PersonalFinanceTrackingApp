from veritabani.baglanti import veritabani_baglan

def gelirleri_listele():
    con = veritabani_baglan()
    if con is None:
        return

    cursor = con.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM gelir ORDER BY tarih DESC")
        gelir_kayitlari = cursor.fetchall()

        if not gelir_kayitlari:
            print("Hiç gelir kaydı bulunamadı.")
            return

        print("\n--- Gelir Kayıtları ---")
        for kayit in gelir_kayitlari:
            print(f"ID: {kayit['id']}, Miktar: {kayit['miktar']} TL, Kategori: {kayit['kategori']}, Tarih: {kayit['tarih']}")

    except Exception as e:
        print(f"Gelirleri listelerken hata oluştu: {e}")
    finally:
        cursor.close()
        con.close()

if __name__ == "__main__":
    gelirleri_listele()