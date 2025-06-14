from flask import request, jsonify, session
from veritabani.baglanti import veritabani_baglan
import hashlib

def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"message": "Eksik bilgi girdiniz!"}), 400

    # Basit hash örneği, isterseniz daha güvenli hale getirebilirsiniz (bcrypt gibi)
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = veritabani_baglan()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM kullanicilar WHERE kullanici_adi = %s", (username,))
    (count,) = cursor.fetchone()

    if count > 0:
        cursor.close()
        conn.close()
        return jsonify({"message": "Bu kullanıcı adı zaten kayıtlı."}), 409

    cursor.execute(
        "INSERT INTO kullanicilar (kullanici_adi, email, sifre) VALUES (%s, %s, %s)",
        (username, email, password_hash)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Kayıt başarılı!"}), 200

def login():
    data = request.get_json()
    username = data.get('username')  # Burayı güncelledik
    password = data.get('password')  # Burayı güncelledik

    user = get_user_by_username(username)
    if user and check_password(user['sifre'], password):
        session['login'] = True
        session['user_id'] = user['id']          # Burayı 'user_id' yap
        session['kullanici_adi'] = user['kullanici_adi']

        return jsonify({"message": "Giriş başarılı"}), 200
    else:
        return jsonify({"message": "Kullanıcı adı veya şifre hatalı"}), 401


def logout():
    user_id = session.get('id')
    if not user_id:
        # 400 değil 200 dön, çünkü zaten çıkış yapılmış sayılır
        return jsonify({'message': 'Zaten çıkış yapmışsınız'}), 200

    db = veritabani_baglan()
    cursor = db.cursor()

    cursor.execute("SELECT login FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()

    if not result:
        cursor.close()
        db.close()
        return jsonify({'message': 'Kullanıcı bulunamadı'}), 404

    login_status = result[0]

    if login_status == 0:
        cursor.close()
        db.close()
        # Burada da 200 dön, zaten çıkış yapılmış
        return jsonify({'message': 'Zaten çıkış yapmışsınız'}), 200

    cursor.execute("UPDATE users SET login = 0 WHERE id = %s", (user_id,))
    db.commit()

    cursor.close()
    db.close()

    session.clear()

    return jsonify({'message': 'Başarıyla çıkış yapıldı'}), 200

def get_user_by_username(username):
    con = veritabani_baglan()
    cursor = con.cursor(dictionary=True)
    query = "SELECT * FROM kullanicilar WHERE kullanici_adi = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    con.close()
    return user  # user dict döner ya da None

def check_password(stored_hash, provided_password):
    import hashlib
    hashed_password = hashlib.sha256(provided_password.encode()).hexdigest()
    return stored_hash == hashed_password

def update_login_status():
    data = request.get_json()
    username = data.get('username')  # Doğru key: "username"
    status = data.get('status')      # Doğru key: "status"

    if username is None or status not in [0, 1]:
        return jsonify({'message': 'Geçersiz veri'}), 400

    try:
        conn = veritabani_baglan()
        cursor = conn.cursor()
        cursor.execute("UPDATE kullanicilar SET login = %s WHERE kullanici_adi = %s", (status, username))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Login durumu güncellendi.'})
    except Exception as e:
        print('DB Hatası:', e)
        return jsonify({'message': 'Veritabanı hatası'}), 500