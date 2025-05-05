from datetime import datetime

def tarih_formatla(tarih_str: str = None) -> str:
    if not tarih_str:
        return datetime.today().strftime('%Y-%m-%d')
    try:
        tarih_obj = datetime.strptime(tarih_str, '%Y-%m-%d')
        return tarih_obj.strftime('%Y-%m-%d')
    except ValueError:
        print("Hatalı tarih formatı! Lütfen 'YYYY-MM-DD' şeklinde girin.")
        return None