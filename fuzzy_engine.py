import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzyPricingEngine:
    def __init__(self):
        # ==========================================
        # 1. SEMESTA PEMBICARAAN (Universe of Discourse)
        # ==========================================
        # Kecepatan (0 - 60 km/jam)
        self.kecepatan = ctrl.Antecedent(np.arange(0, 61, 1), 'kecepatan')
        # Jarak Tempuh (0 - 50 km)
        self.jarak = ctrl.Antecedent(np.arange(0, 51, 1), 'jarak')
        # Faktor Pengali Harga (1.0x - 3.0x)
        self.pengali = ctrl.Consequent(np.arange(1.0, 3.1, 0.1), 'pengali')

        # ==========================================
        # 2. FUNGSI KEANGGOTAAN (Membership Functions)
        # ==========================================
        # Kurva Kecepatan
        self.kecepatan['macet'] = fuzz.trimf(self.kecepatan.universe, [0, 0, 20])
        self.kecepatan['ramai_lancar'] = fuzz.trimf(self.kecepatan.universe, [10, 30, 50])
        self.kecepatan['lancar'] = fuzz.trapmf(self.kecepatan.universe, [40, 50, 60, 60])

        # Kurva Jarak
        self.jarak['dekat'] = fuzz.trimf(self.jarak.universe, [0, 0, 15])
        self.jarak['sedang'] = fuzz.trimf(self.jarak.universe, [10, 25, 40])
        self.jarak['jauh'] = fuzz.trapmf(self.jarak.universe, [30, 40, 50, 50])

        # Kurva Output (Faktor Pengali Harga)
        self.pengali['normal'] = fuzz.trimf(self.pengali.universe, [1.0, 1.0, 1.5])
        self.pengali['naik_sedang'] = fuzz.trimf(self.pengali.universe, [1.3, 1.8, 2.3])
        self.pengali['surge_pricing'] = fuzz.trimf(self.pengali.universe, [2.0, 3.0, 3.0])

        # ==========================================
        # 3. RULE BASE (Aturan Mamdani)
        # ==========================================
        rule1 = ctrl.Rule(self.kecepatan['macet'] & self.jarak['jauh'], self.pengali['surge_pricing'])
        rule2 = ctrl.Rule(self.kecepatan['macet'] & self.jarak['dekat'], self.pengali['naik_sedang'])
        rule3 = ctrl.Rule(self.kecepatan['ramai_lancar'] & self.jarak['sedang'], self.pengali['naik_sedang'])
        rule4 = ctrl.Rule(self.kecepatan['lancar'] & self.jarak['dekat'], self.pengali['normal'])
        rule5 = ctrl.Rule(self.kecepatan['lancar'] & self.jarak['jauh'], self.pengali['naik_sedang'])
        
        # Tambahan rule agar lebih cover banyak kemungkinan
        rule6 = ctrl.Rule(self.kecepatan['ramai_lancar'] & self.jarak['dekat'], self.pengali['normal'])
        rule7 = ctrl.Rule(self.kecepatan['macet'] & self.jarak['sedang'], self.pengali['surge_pricing'])

        # ==========================================
        # 4. MESIN INFERENSI
        # ==========================================
        self.pricing_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
        self.pricing_sim = ctrl.ControlSystemSimulation(self.pricing_ctrl)

    def hitung_pengali(self, input_kecepatan, input_jarak):
        """Fungsi untuk memasukkan Crisp Input dan menghasilkan Crisp Output"""
        # Mencegah error jika angka melebihi batas kurva (misal kecepatan 70 diubah jadi 60)
        input_kecepatan = max(0, min(60, input_kecepatan))
        input_jarak = max(0, min(50, input_jarak))

        # Masukkan nilai ke dalam sistem fuzzy
        self.pricing_sim.input['kecepatan'] = input_kecepatan
        self.pricing_sim.input['jarak'] = input_jarak

        # Hitung Defuzzifikasi (Metode Centroid / Titik Berat)
        self.pricing_sim.compute()
        
        # Kembalikan hasilnya dengan pembulatan 2 angka di belakang koma
        return round(self.pricing_sim.output['pengali'], 2)

# ==========================================
# BLOK PENGUJIAN LOGIKA FUZZY
# ==========================================
if __name__ == '__main__':
    mesin_fuzzy = FuzzyPricingEngine()
    print("🧠 Menjalankan Simulasi Otak AI (Logika Fuzzy Mamdani)...")
    
    # Kita pura-puranya menggunakan kecepatan 15.68 km/jam dari database tadi
    test_speed = 15.68 
    # Kita pura-puranya jarak pengirimannya lumayan jauh (35 km)
    test_jarak = 35.0  
    
    print(f"Input -> Kecepatan: {test_speed} km/jam (Macet) | Jarak: {test_jarak} km (Jauh/Sedang)")
    
    # Menghitung hasilnya
    hasil_pengali = mesin_fuzzy.hitung_pengali(test_speed, test_jarak)
    print(f"🔥 HASIL: Faktor Pengali Harga = {hasil_pengali}x")