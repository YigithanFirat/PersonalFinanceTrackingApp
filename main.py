from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from veritabani.baglanti import veritabani_baglan
from veritabani.register_login import register, login, logout, update_login_status
from gelir.ekle import gelir_ekle
from gelir.listele import gelir_listele
from gelir.sil_guncelle import gelir_sil, gelir_guncelle
from gider.ekle import gider_ekle
from gider.listele import giderleri_listele
from gider.sil_guncelle import gider_guncelle, gider_sil
from raporlar.grafik_olustur import gelir_gider_karsilastir, gelir_grafik, gider_grafik

app = Flask(__name__)
app.secret_key = 'Abusivesnake'  # Session için gerekli

CORS(app, supports_credentials=True)

@app.route('/')
def index():
    login_durumu = "bil" if session.get('login') else ""
    return render_template("index.html", login_durumu=login_durumu)

@app.route('/api/gelir/ekle', methods=['POST'])
def gelir_ekle_route():
    return gelir_ekle()

@app.route('/api/gelir/listele', methods=['GET'])
def gelir_listele_route():
    return gelir_listele()

@app.route('/api/gelir/sil/<int:id>', methods=['DELETE'])
def gelir_sil_route(id):
    return gelir_sil(id)

@app.route('/api/gelir/guncelle/<int:id>', methods=['PUT'])
def gelir_guncelle_route(id):
    return gelir_guncelle(id)

@app.route('/api/gider/ekle', methods=['POST'])
def gider_ekle_route():
    return gider_ekle()

@app.route('/api/gider/listele', methods=['GET'])
def giderleri_listele_route():
    return giderleri_listele()

@app.route('/api/gider/sil/<int:id>', methods=['DELETE'])
def gider_sil_route(id):
    return gider_sil(id)

@app.route('/api/gider/guncelle/<int:id>', methods=['PUT'])
def gider_guncelle_route(id):
    return gider_guncelle(id)

@app.route('/update_login_status', methods=['POST'])
def update_login_status_route():
    return update_login_status()

@app.route('/api/grafik/gelir')
def api_gelir_grafik():
    return gelir_grafik()

@app.route('/api/grafik/gider')
def api_gider_grafik():
    return gider_grafik()

@app.route('/api/grafik/karsilastir')
def api_gelir_gider_karsilastir():
    return gelir_gider_karsilastir()

@app.route('/login', methods=['POST'])
def login_route():
    return login()

@app.route('/register', methods=['POST'])
def register_user():
    return register()

@app.route('/logout', methods=['POST'])
def logout_route():
    session.clear()
    return logout()

@app.route('/check_username', methods=['POST'])
def check_username():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({'error': 'Username gerekli'}), 400

    conn = veritabani_baglan()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM kullanicilar WHERE kullanici_adi = %s", (username,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return jsonify({'exists': True, 'id': result[0]})
    else:
        return jsonify({'exists': False})

@app.route('/api/transactions', methods=['GET'])
def tum_islemler():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Giriş yapılmamış'}), 401

    conn = veritabani_baglan()
    if not conn:
        return jsonify({'error': 'Veritabanına bağlanılamadı'}), 500

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, miktar, kategori, tarih, kullanici_id
        FROM gelir
        WHERE kullanici_id = %s
    """, (user_id,))
    gelirler = cursor.fetchall()

    cursor.execute("""
        SELECT id, miktar, kategori, aciklama, tarih, kullanici_id
        FROM gider
        WHERE kullanici_id = %s
    """, (user_id,))
    giderler = cursor.fetchall()

    cursor.close()
    conn.close()

    giderler_formatted = [
        {
            "id": g["id"],
            "amount": float(g["miktar"]),
            "category": f"{g['kategori']} ({g['aciklama']})" if g.get("aciklama") else g["kategori"],
            "date": g["tarih"].strftime("%Y-%m-%d"),
            "user_id": g["kullanici_id"],
            "type": "Gider"
        }
        for g in giderler
    ]

    gelirler_formatted = [
        {
            "id": g["id"],
            "amount": float(g["miktar"]),
            "category": g["kategori"],
            "date": g["tarih"].strftime("%Y-%m-%d"),
            "user_id": g["kullanici_id"],
            "type": "Gelir"
        }
        for g in gelirler
    ]

    tum = gelirler_formatted + giderler_formatted
    tum.sort(key=lambda x: x["date"], reverse=True)

    return jsonify(tum)

@app.route('/grafik')
def grafik():
    return render_template('grafik.html')

if __name__ == "__main__":
    app.run(debug=True)