# TÜRKÇE

## 💰 Kişisel Finans Takip Uygulaması

Bu Python projesi, kişisel gelir ve giderlerinizi yönetmenize, veritabanında saklamanıza ve aylık bazda grafiksel raporlar oluşturmanıza yardımcı olur. Kullanıcı dostu komut satırı menüsüyle tüm işlemler kolayca yapılabilir.

### 🚀 Proje Özellikleri

- 💵 Gelir ve gider ekleme, silme, güncelleme ve listeleme
- 📊 Aylık gelir, gider ve karşılaştırmalı grafik raporları (Matplotlib ile)
- 🗓️ Otomatik tarih formatlama ve doğrulama
- 🗂️ Modüler dosya yapısı ile okunabilir ve genişletilebilir mimari
- 🗃️ MySQL veritabanı ile veri kalıcılığı

### 🧱 Proje Klasör Yapısı

├── main.py # Ana uygulama dosyası (menü arayüzü)
├── gelir/
│ ├── ekle.py # Gelir ekleme fonksiyonu
│ ├── listele.py # Gelirleri listeleme fonksiyonu
│ └── sil_guncelle.py # Gelirleri silme ve güncelleme fonksiyonu
├── gider/
│ ├── ekle.py # Gider ekleme fonksiyonu
│ ├── listele.py # Giderleri listeleme fonksiyonu
│ └── sil_guncelle.py # Giderleri silme ve güncelleme fonksiyonu
├── raporlar/
│ └── grafik_olustur.py # Gelir/Gider grafik raporları
├── utils/
│ └── tarih_formatla.py # Tarih formatlama ve doğrulama yardımcı fonksiyonu
└── README.md # Bu dosya


### ⚙️ Gereksinimler

- Python 3.8 veya üzeri
- MySQL veritabanı
- Python bağımlılıkları:
  - `mysql-connector-python`
  - `matplotlib`

### 💾 Kurulum

```bash
git clone https://github.com/YigithanFirat/PersonalFinanceTrackingApp.git
cd PersonalFinanceTrackingApp
pip install mysql-connector-python matplotlib
python main.py
```

### 📈 Grafiksel Raporlar
Aylık Gelir Grafiği: Her ayın toplam gelirleri
Aylık Gider Grafiği: Her ayın toplam giderleri
Aylık Karşılaştırmalı Grafik: Gelir ve giderlerin aylık karşılaştırması

### 📌 Notlar
Tarih formatı: YYYY-MM-DD
Hatalı veya boş bırakılan tarih girişlerinde otomatik olarak bugünün tarihi kullanılır.
Veritabanı bağlantı bilgilerinizi gizli tutmayı unutmayın.

### 👨‍💻 Geliştirici
Bu proje bireysel bir Python öğrenme ve uygulama sürecinin parçası olarak geliştirilmiştir.
Geri bildirim, katkı ya da iletişim için GitHub üzerinden ulaşabilirsiniz.

# ENGLISH

## 💰 Personal Finance Tracking Application

This Python project helps you manage your personal income and expenses, store them in a database, and generate graphical reports on a monthly basis. With a user-friendly command-line menu, all operations can be performed easily.

### 🚀 Project Features

- 💵 Add, delete, update, and list income and expenses
- 📊 Monthly income, expense, and comparative chart reports (with Matplotlib)
- 🗓️ Automatic date formatting and validation
- 🗂️ Modular file structure for readable and extendable architecture
- 🗃️ Data persistence with MySQL database

### 🧱 Project Folder Structure

├── main.py                       # Main application file (menu interface)  
├── gelir/  
│   ├── ekle.py                   # Function to add income  
│   ├── listele.py                # Function to list income  
│   └── sil_guncelle.py           # Functions to delete/update income  
├── gider/  
│   ├── ekle.py                   # Function to add expenses  
│   ├── listele.py                # Function to list expenses  
│   └── sil_guncelle.py           # Functions to delete/update expenses  
├── raporlar/  
│   └── grafik_olustur.py         # Graph reports for income/expenses  
├── utils/  
│   └── tarih_formatla.py         # Helper for date formatting and validation  
└── README.md                     # This file  

### ⚙️ Requirements

- Python 3.8 or above  
- MySQL database  
- Python dependencies:  
  - `mysql-connector-python`  
  - `matplotlib`  

### 💾 Installation

```bash
git clone https://github.com/YigithanFirat/PersonalFinanceTrackingApp.git
cd PersonalFinanceTrackingApp
pip install mysql-connector-python matplotlib
python main.py
```

### 📈 Graphical Reports
Monthly Income Chart: Total income per month
Monthly Expense Chart: Total expenses per month
Monthly Comparative Chart: Comparison of income and expenses by month

### 📌 Notes
Date format: YYYY-MM-DD
If the entered date is incorrect or left blank, today's date will be used automatically.
Don't forget to keep your database credentials secure.

### 👨‍💻 Developer
This project was developed as part of an individual learning and practice process with Python.
For feedback, contributions, or contact, feel free to reach out via GitHub.