from veritabani.baglanti import veritabani_baglan
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS açıldı

@app.route('/api/gelir/listele', methods=['GET'])
def gelir_listele():
    con = veritabani_baglan()
    if not con:
        return jsonify({"success": False, "message": "Veritabanı bağlantısı başarısız"})
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gelir ORDER BY tarih DESC")
    gelirler = cursor.fetchall()
    cursor.close()
    con.close()
    return jsonify({"success": True, "data": gelirler})