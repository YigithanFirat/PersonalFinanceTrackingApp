from datetime import datetime
from typing import Optional

def tarih_formatla(tarih_str: Optional[str] = None) -> Optional[str]:
    """
    Gelen tarih stringini 'YYYY-MM-DD' formatına çevirir.
    Eğer tarih_str None ise bugünün tarihini döner.
    Hatalı format gelirse None döner ve uyarı verir.
    """
    if not tarih_str:
        return datetime.today().strftime('%Y-%m-%d')
    try:
        tarih_obj = datetime.strptime(tarih_str, '%Y-%m-%d')
        return tarih_obj.strftime('%Y-%m-%d')
    except ValueError:
        # print yerine uyarı mesajı olarak logging kullanılabilir, ya da exception fırlatılabilir.
        print("Hatalı tarih formatı! Lütfen 'YYYY-MM-DD' şeklinde girin.")
        return None