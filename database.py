import mysql.connector
from mysql.connector import Error

class QueryHandler:
    def __init__(self):
        # Kredensial default XAMPP/Laragon
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'db_fuzzy_transjakarta'

    def connect(self):
        """Membuat koneksi ke database MySQL"""
        try:
            return mysql.connector.connect(
                host=self.host, 
                user=self.user, 
                password=self.password, 
                database=self.database
            )
        except Error as e:
            print(f"❌ Error Database: {e}")
            return None

    def get_rata_rata_kecepatan(self, koridor):
        """Menarik rata-rata kecepatan bus di suatu koridor (sebagai Crisp Input)"""
        conn = self.connect()
        if conn is None: 
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            # Query untuk menghitung rata-rata kecepatan di rute tersebut (mengabaikan speed 0)
            query = """
                SELECT ROUND(AVG(speed), 2) AS rata_rata_speed
                FROM log_gps_transjakarta
                WHERE corridor = %s AND speed > 0;
            """
            cursor.execute(query, (koridor,))
            result = cursor.fetchone()
            
            # Jika rute ditemukan dan ada datanya, kembalikan angkanya. Jika tidak, return None
            if result and result['rata_rata_speed'] is not None:
                return float(result['rata_rata_speed'])
            else:
                return None
                
        except Error as e:
            print(f"❌ Error saat SELECT data: {e}")
            return None
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def simpan_transaksi(self, koridor, jarak, kecepatan, pengali, tarif):
        """Menyimpan hasil perhitungan ke tabel transaksi"""
        conn = self.connect()
        if conn is None: 
            return

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO transaksi_harga_dinamis 
                (corridor, jarak_pengiriman_km, rata_rata_speed, faktor_pengali_fuzzy, tarif_akhir) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (koridor, jarak, kecepatan, pengali, tarif))
            conn.commit()
            print("✅ Transaksi berhasil disimpan ke Database!")
        except Error as e:
            print(f"❌ Error saat INSERT data: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

# ==========================================
# BLOK PENGUJIAN KONEKSI
# ==========================================
if __name__ == '__main__':
    print("Mencoba menyambungkan Python ke MySQL...")
    db = QueryHandler()
    
    # Kita coba tarik data kecepatan dari Koridor '1'
    koridor_test = '1'
    kecepatan = db.get_rata_rata_kecepatan(koridor_test)
    
    if kecepatan is not None:
        print(f"✅ KONEKSI SUKSES! Rata-rata kecepatan armada di Koridor {koridor_test} adalah: {kecepatan} km/jam")
    else:
        print(f"⚠️ Koneksi gagal, atau tidak ada data armada di Koridor {koridor_test}.")