# 💰 Kişisel Finans Takip Uygulaması

Bu Python projesi, kişisel gelir ve giderlerinizi yönetmenize, veritabanında saklamanıza ve aylık bazda grafiksel raporlar oluşturmanıza yardımcı olur. Kullanıcı dostu komut satırı menüsüyle tüm işlemler kolayca yapılabilir.

## 🚀 Proje Özellikleri

- 💵 Gelir ve gider ekleme, silme, güncelleme ve listeleme
- 📊 Aylık gelir, gider ve karşılaştırmalı grafik raporları (Matplotlib ile)
- 🗓️ Otomatik tarih formatlama ve doğrulama
- 🗂️ Modüler dosya yapısı ile okunabilir ve genişletilebilir mimari
- 🗃️ MySQL veritabanı ile veri kalıcılığı

## 🧱 Proje Klasör Yapısı

├── main.py # Ana uygulama dosyası (menü arayüzü)
├── gelir/
│ ├── ekle.py # Gelir ekleme fonksiyonu
│ ├── listele.py # Gelirleri listeleme fonksiyonu
│ └── sil_guncelle.py # Gelir silme/güncelleme işlemleri
├── gider/
│ ├── ekle.py # Gider ekleme fonksiyonu
│ ├── listele.py # Giderleri listeleme fonksiyonu
│ └── sil_guncelle.py # Gider silme/güncelleme işlemleri
├── raporlar/
│ └── grafik_olustur.py # Gelir/gider grafik raporları
├── utils/
│ └── tarih_formatla.py # Tarih formatlama ve doğrulama yardımcı fonksiyonu
└── README.md # Bu dosya

## ⚙️ Gereksinimler

- Python 3.8 veya üzeri
- MySQL veritabanı
- Python bağımlılıkları:
  - `mysql-connector-python`
  - `matplotlib`

## 💾 Kurulum

```bash
git clone https://github.com/YigithanFirat/PersonalFinanceTrackingApp.git
cd PersonalFinanceTrackingApp
pip install mysql-connector-python matplotlib
python main.py

📈 Grafiksel Raporlar
Aylık Gelir Grafiği: Her ayın toplam gelirleri

Aylık Gider Grafiği: Her ayın toplam giderleri

Aylık Karşılaştırmalı Grafik: Gelir ve giderlerin aylık karşılaştırması

🗃️ Veritabanı Şeması
Aşağıda uygulamada kullanılan temel MySQL veritabanı şeması yer almaktadır:
veritabani_sablon.png


📌 Notlar
Tarih formatı: YYYY-MM-DD

Hatalı veya boş bırakılan tarih girişlerinde otomatik olarak bugünün tarihi kullanılır.

Veritabanı bağlantı bilgilerinizi gizli tutmayı unutmayın.

👨‍💻 Geliştirici
Bu proje bireysel bir Python öğrenme ve uygulama sürecinin parçası olarak geliştirilmiştir.
Geri bildirim, katkı ya da iletişim için GitHub üzerinden ulaşabilirsiniz.