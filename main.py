from database import QueryHandler
from fuzzy_engine import FuzzyPricingEngine

def jalankan_sistem():
    print("="*50)
    print("🚚 SISTEM DYNAMIC PRICING LOGISTIK (FUZZY MAMDANI)")
    print("="*50)
    
    # 1. Minta Input dari Pengguna (Simulasi ada pesanan masuk)
    koridor = input("Masukkan Rute/Koridor Bus (contoh: 1, 8D, 9): ")
    try:
        jarak_km = float(input("Masukkan Jarak Pengiriman (dalam km): "))
    except ValueError:
        print("❌ Error: Jarak harus berupa angka!")
        return

    print("\n[PROSES BERJALAN] ⏳")

    # 2. Inisialisasi Modul
    db = QueryHandler()
    fuzzy = FuzzyPricingEngine()

    # 3. Ekstrak Data Kemacetan dari MySQL
    print(f"1️⃣ Menarik data kecepatan armada di Koridor {koridor} dari MySQL...")
    kecepatan_db = db.get_rata_rata_kecepatan(koridor)
    
    if kecepatan_db is None:
        print(f"⚠️ Rute {koridor} tidak ditemukan di database. Menggunakan kecepatan standar 25 km/jam.")
        kecepatan_db = 25.0
        
    print(f"   -> Rata-rata Kecepatan Saat Ini: {kecepatan_db} km/jam")

    # 4. Proses Mesin AI (Fuzzy Logic)
    print("2️⃣ Memasukkan data ke Mesin AI Logika Fuzzy...")
    faktor_pengali = fuzzy.hitung_pengali(kecepatan_db, jarak_km)
    print(f"   -> 🔥 Faktor Pengali Harga (Output Fuzzy): {faktor_pengali}x")

    # 5. Kalkulasi Harga Akhir
    print("3️⃣ Menghitung Tarif Dinamis...")
    TARIF_DASAR_PER_KM = 2500  # Asumsi Rp 2.500 per kilometer
    tarif_awal = jarak_km * TARIF_DASAR_PER_KM
    tarif_akhir = tarif_awal * faktor_pengali

    print("\n" + "="*50)
    print("🧾 RINGKASAN TRANSAKSI PESANAN")
    print("="*50)
    print(f"Rute/Koridor        : {koridor}")
    print(f"Jarak Pengiriman    : {jarak_km} km")
    print(f"Kondisi Lalu Lintas : {kecepatan_db} km/jam")
    print(f"Tarif Normal        : Rp {tarif_awal:,.2f}")
    print(f"Tarif Dinamis Akhir : Rp {tarif_akhir:,.2f} (Dikali {faktor_pengali}x)")
    print("="*50)

    # 6. Simpan Bukti Transaksi ke MySQL
    print("\n4️⃣ Menyimpan rekam transaksi ke Database...")
    db.simpan_transaksi(koridor, jarak_km, kecepatan_db, faktor_pengali, tarif_akhir)
    print("\nSistem Selesai. Terima kasih!")

if __name__ == '__main__':
    jalankan_sistem()