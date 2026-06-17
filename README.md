# 🚚 Sistem Dynamic Pricing Logistik Berbasis Logika Fuzzy (Mamdani)

Proyek ini merupakan simulasi algoritma **Dynamic Pricing (Surge Pricing)** pada layanan logistik dan transportasi menggunakan **Logika Fuzzy Metode Mamdani**. Sistem menentukan faktor pengali harga berdasarkan dua variabel utama:

- 📍 **Jarak Pengiriman**
- 🚦 **Kondisi Lalu Lintas (Rata-rata Kecepatan Kendaraan)**

Untuk menghasilkan simulasi yang lebih realistis, sistem terintegrasi dengan **Dataset GPS Transjakarta** yang berisi lebih dari **775.000 titik koordinat historis armada bus** sebagai indikator kemacetan spasial.

---

# 🛠️ Tech Stack

| Teknologi | Digunakan Untuk |
|-----------|----------------|
| Python 3 | Bahasa Pemrograman Utama |
| MySQL | Penyimpanan Data |
| Scikit-Fuzzy | Mesin Inferensi Fuzzy Mamdani |
| NumPy | Operasi Numerik |
| NetworkX | Pemodelan dan Analisis Jaringan |
| MySQL Connector | Koneksi Python ke Database |

---

# 📋 Prasyarat (Prerequisites)

Sebelum menjalankan aplikasi, pastikan komputer Anda telah terinstal:

- Python 3.x
- XAMPP atau Laragon
- Git

Untuk memastikan instalasi berhasil, jalankan:

```bash
python --version
git --version
```

---

# ⚙️ Cara Instalasi dan Setup

## 1️⃣ Clone Repository

Clone repository ke komputer lokal:

```bash
git clone https://github.com/username-kamu/nama-repo-kamu.git
```

Masuk ke folder project:

```bash
cd nama-repo-kamu
```

---

## 2️⃣ Persiapan Database MySQL

### Menjalankan Server Database

Nyalakan layanan MySQL melalui:

- XAMPP → Start pada modul **MySQL**
- Laragon → Start All

---

### Membuat Database

Masuk ke MySQL:

```bash
mysql -u root -p
```

Buat database baru:

```sql
CREATE DATABASE db_fuzzy_transjakarta;
USE db_fuzzy_transjakarta;
```

---

### Import Dataset GPS

Unduh dataset:

```text
transjakarta_gps.csv
```

Lalu letakkan file tersebut pada lokasi yang dapat diakses oleh MySQL.

Contoh:

```text
C:\xampp\mysql\data\
```

atau

```text
C:\laragon\data\
```

---

### Membuat Tabel

Buat tabel berikut sesuai skema DDL proyek:

- `log_gps_transjakarta`
- `transaksi_harga_dinamis`

Contoh struktur:

```sql
CREATE TABLE log_gps_transjakarta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    koridor VARCHAR(20),
    latitude DOUBLE,
    longitude DOUBLE,
    speed DOUBLE,
    timestamp DATETIME
);

CREATE TABLE transaksi_harga_dinamis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    koridor VARCHAR(20),
    jarak_km DOUBLE,
    kecepatan_rata_rata DOUBLE,
    faktor_harga DOUBLE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Memasukkan Dataset ke Database

Import dataset menggunakan:

```sql
LOAD DATA INFILE 'C:/xampp/mysql/data/transjakarta_gps.csv'
INTO TABLE log_gps_transjakarta
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

> **Catatan:** Sesuaikan lokasi file CSV dengan direktori pada komputer Anda.

---

## 3️⃣ Instalasi Library Python

Buka terminal pada folder project:

```bash
cd nama-repo-kamu
```

Kemudian install seluruh dependency:

```bash
pip install mysql-connector-python scikit-fuzzy numpy networkx
```

Atau install sekaligus melalui file requirements:

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Konfigurasi Koneksi Database

Secara default, program menggunakan konfigurasi:

```python
host = "localhost"
user = "root"
password = ""
database = "db_fuzzy_transjakarta"
```

Jika MySQL Anda menggunakan password, sesuaikan konfigurasi pada file:

```text
database.py
```

Contoh:

```python
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "password_mysql_anda",
    "database": "db_fuzzy_transjakarta"
}
```

---

# 🚀 Cara Menjalankan Aplikasi

Pastikan:

- MySQL telah aktif
- Dataset berhasil diimport
- Seluruh library telah terinstal

Kemudian jalankan program:

```bash
python main.py
```

---

# 📖 Alur Penggunaan Sistem

### 1. Input Koridor/Rute

Contoh:

```text
Masukkan Koridor : 1
```

atau

```text
Masukkan Koridor : 8D
```

---

### 2. Input Jarak Pengiriman

Contoh:

```text
Masukkan Jarak Pengiriman (km) : 12
```

---

### 3. Pengambilan Data Kemacetan

Sistem akan:

- Mengakses database MySQL
- Mengambil data GPS historis Transjakarta
- Menghitung rata-rata kecepatan armada pada koridor tersebut

---

### 4. Proses Inferensi Fuzzy Mamdani

Mesin Fuzzy akan mengevaluasi:

- Jarak Pengiriman
- Rata-rata Kecepatan Kendaraan

Kemudian menghasilkan:

```text
Faktor Pengali Harga (Surge Pricing)
```

Contoh:

```text
Kondisi Lalu Lintas : Macet
Faktor Harga        : 1.5x
```

---

### 5. Penyimpanan Transaksi

Setiap simulasi akan disimpan secara otomatis ke dalam tabel:

```text
transaksi_harga_dinamis
```

Data yang disimpan meliputi:

- Koridor
- Jarak Pengiriman
- Kecepatan Rata-rata
- Faktor Harga
- Waktu Transaksi

---

# 📂 Struktur Proyek (Contoh)

```text
nama-repo/
│
├── main.py
├── database.py
├── fuzzy_engine.py
├── requirements.txt
├── README.md
└── dataset/
    └── transjakarta_gps.csv
```

---

# 🎯 Fitur Utama

✅ Integrasi Dataset GPS Transjakarta  
✅ Perhitungan Dynamic Pricing berbasis Fuzzy Mamdani  
✅ Analisis kondisi lalu lintas berdasarkan data historis  
✅ Penyimpanan histori transaksi ke MySQL  
✅ Simulasi harga logistik secara otomatis

---

# 👨‍💻 Dibuat Untuk

**Proyek Sistem Dynamic Pricing Logistik Berbasis Logika Fuzzy (Mamdani)**

Mengimplementasikan konsep:

- Artificial Intelligence
- Fuzzy Logic (Mamdani)
- Dynamic Pricing
- Database Integration
- Data-Driven Transportation Analysis

🚚📊🧠