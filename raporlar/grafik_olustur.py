from veritabani.baglanti import veritabani_baglan
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def veri_cek(tablo_adi):
    con = veritabani_baglan()
    query = f"SELECT miktar, tarih FROM {tablo_adi}"
    df = pd.read_sql(query, con)
    con.close()
    return df

def aylik_toplam(df):
    df['tarih'] = pd.to_datetime(df['tarih'])
    df = df.groupby(df['tarih'].dt.to_period('M'))['miktar'].sum().reset_index()
    df['tarih'] = df['tarih'].astype(str)
    return df

def grafik_png_olarak_olustur(df, title, label, color='blue'):
    plt.figure(figsize=(10, 5))
    plt.plot(df['tarih'], df['miktar'], marker='o', label=label, color=color)
    plt.title(title)
    plt.xlabel("Tarih")
    plt.ylabel("Tutar")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return img_base64

def gelir_grafik():
    df = veri_cek("gelir")
    df = aylik_toplam(df)
    return grafik_png_olarak_olustur(df, "Aylık Gelir Grafiği", "Gelir", color='green')

def gider_grafik():
    df = veri_cek("gider")
    df = aylik_toplam(df)
    return grafik_png_olarak_olustur(df, "Aylık Gider Grafiği", "Gider", color='red')

def gelir_gider_karsilastir():
    df_gelir = aylik_toplam(veri_cek("gelir"))
    df_gider = aylik_toplam(veri_cek("gider"))
    df = pd.merge(df_gelir, df_gider, on='tarih', how='outer', suffixes=('_gelir', '_gider')).fillna(0)

    plt.figure(figsize=(10, 5))
    plt.plot(df['tarih'], df['miktar_gelir'], marker='o', label='Gelir', color='green')
    plt.plot(df['tarih'], df['miktar_gider'], marker='o', label='Gider', color='red')
    plt.title("Aylık Gelir-Gider Karşılaştırması")
    plt.xlabel("Tarih")
    plt.ylabel("Tutar")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return img_base64