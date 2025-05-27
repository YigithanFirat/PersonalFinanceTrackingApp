from flask import jsonify
from collections import defaultdict
from veritabani.baglanti import veritabani_baglan

def gelir_grafik():
    con = veritabani_baglan()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT DATE_FORMAT(tarih, '%Y-%m') as ay, SUM(miktar) as toplam 
        FROM gelir 
        GROUP BY ay ORDER BY ay
    """)
    rows = cursor.fetchall()
    cursor.close()
    con.close()

    labels = [row['ay'] for row in rows]
    data = [float(row['toplam']) for row in rows]
    return jsonify({'labels': labels, 'data': data})

def gider_grafik():
    con = veritabani_baglan()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT DATE_FORMAT(tarih, '%Y-%m') as ay, SUM(miktar) as toplam 
        FROM gider 
        GROUP BY ay ORDER BY ay
    """)
    rows = cursor.fetchall()
    cursor.close()
    con.close()

    labels = [row['ay'] for row in rows]
    data = [float(row['toplam']) for row in rows]
    return jsonify({'labels': labels, 'data': data})

def gelir_gider_karsilastir():
    con = veritabani_baglan()
    cursor = con.cursor(dictionary=True)

    cursor.execute("""
        SELECT DATE_FORMAT(tarih, '%Y-%m') as ay, 'gelir' as tip, SUM(miktar) as toplam
        FROM gelir GROUP BY ay
        UNION ALL
        SELECT DATE_FORMAT(tarih, '%Y-%m') as ay, 'gider' as tip, SUM(miktar) as toplam
        FROM gider GROUP BY ay
        ORDER BY ay
    """)
    rows = cursor.fetchall()
    cursor.close()
    con.close()

    data_dict = defaultdict(lambda: {'gelir': 0, 'gider': 0})
    for row in rows:
        data_dict[row['ay']][row['tip']] = float(row['toplam'])

    labels = sorted(data_dict.keys())
    gelirData = [data_dict[ay]['gelir'] for ay in labels]
    giderData = [data_dict[ay]['gider'] for ay in labels]

    return jsonify({'labels': labels, 'gelirData': gelirData, 'giderData': giderData})