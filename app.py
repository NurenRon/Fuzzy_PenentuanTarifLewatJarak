from flask import Flask, render_template, request, jsonify
from database import QueryHandler
from fuzzy_engine import FuzzyPricingEngine

app = Flask(__name__)
db = QueryHandler()
fuzzy = FuzzyPricingEngine()

@app.route('/')
def index():
    riwayat = db.get_riwayat_transaksi(limit=5)
    return render_template('index.html', riwayat=riwayat)

@app.route('/api/hitung', methods=['POST'])
def hitung_tarif():
    data = request.json
    koridor = data.get('koridor')
    try:
        jarak_km = float(data.get('jarak', 0))
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Jarak tidak valid'})

    kecepatan_db = db.get_rata_rata_kecepatan(koridor)
    if kecepatan_db is None:
        kecepatan_db = 25.0  

    faktor_pengali = fuzzy.hitung_pengali(kecepatan_db, jarak_km)

    TARIF_DASAR_PER_KM = 2500
    tarif_awal = jarak_km * TARIF_DASAR_PER_KM
    tarif_akhir = tarif_awal * faktor_pengali

    db.simpan_transaksi(koridor, jarak_km, kecepatan_db, faktor_pengali, tarif_akhir)

    return jsonify({
        'status': 'success',
        'kecepatan': kecepatan_db,
        'pengali': faktor_pengali,
        'tarif_awal': tarif_awal,
        'tarif_akhir': tarif_akhir
    })

if __name__ == '__main__':
    print("🚀 Server berjalan di http://127.0.0.1:8081")
    app.run(debug=True, port=8081)