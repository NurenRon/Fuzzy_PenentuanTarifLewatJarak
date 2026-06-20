import mysql.connector
from mysql.connector import Error

class QueryHandler:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'db_fuzzy_transjakarta'

    def connect(self):
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
        conn = self.connect()
        if conn is None: 
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT ROUND(AVG(speed), 2) AS rata_rata_speed
                FROM log_gps_transjakarta
                WHERE corridor = %s AND speed > 0;
            """
            cursor.execute(query, (koridor,))
            result = cursor.fetchone()
            
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

    def get_riwayat_transaksi(self, limit=5):
        conn = self.connect()
        if conn is None: 
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT * FROM transaksi_harga_dinamis 
                ORDER BY id DESC LIMIT %s
            """
            cursor.execute(query, (limit,))
            return cursor.fetchall()
        except Error as e:
            print(f"❌ Error saat SELECT riwayat: {e}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()