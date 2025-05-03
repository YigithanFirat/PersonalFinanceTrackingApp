from baglanti import veritabani_baglan

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
        return

    cursor = con.cursor()
    
    # Tabloları oluştur
    gelir_tablosu_olustur(cursor)
    gider_tablosu_olustur(cursor)

    con.commit()  # Değişiklikleri kaydet
    cursor.close()
    con.close()
    print("Tüm tablolar başarıyla oluşturuldu.")

if __name__ == "__main__":
    tum_tablolari_olustur()