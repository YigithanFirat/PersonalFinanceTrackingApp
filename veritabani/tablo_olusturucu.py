from veritabani.baglanti import veritabani_baglan

def gelir_tablosu_olustur(cursor):
    """Gelir tablosunu oluşturur."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gelir (
            id INT AUTO_INCREMENT PRIMARY KEY,
            miktar DECIMAL(10,2) NOT NULL,
            kategori VARCHAR(255),
            tarih DATE DEFAULT CURRENT_DATE
        )
    """)

def gider_tablosu_olustur(cursor):
    """Gider tablosunu oluşturur."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gider (
            id INT AUTO_INCREMENT PRIMARY KEY,
            miktar DECIMAL(10,2) NOT NULL,
            kategori VARCHAR(255),
            aciklama TEXT,
            tarih DATE DEFAULT CURRENT_DATE
        )
    """)

def tum_tablolari_olustur():
    """Gelir ve gider tablolarını oluşturur."""
    con = veritabani_baglan()
    if con is None:
        print("Veritabanı bağlantısı kurulamadı, tablolar oluşturulamadı.")
        return

    try:
        cursor = con.cursor()
        gelir_tablosu_olustur(cursor)
        gider_tablosu_olustur(cursor)
        con.commit()
        print("Tüm tablolar başarıyla oluşturuldu.")
    except Exception as e:
        print(f"Tablo oluşturma sırasında hata oluştu: {e}")
    finally:
        if cursor:
            cursor.close()
        con.close()

if __name__ == "__main__":
    tum_tablolari_olustur()