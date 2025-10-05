import requests
import json
from datetime import datetime, timedelta

# --- NASA API Ayarları ---
# NASA'dan ücretsiz olarak kendi API anahtarınızı alabilirsiniz: https://api.nasa.gov/
NASA_API_KEY = 'DEMO_KEY' # Kendi API anahtarınızı buraya yapıştırın. DEMO_KEY sınırlı kullanım sunar.
NASA_API_URL = 'https://api.nasa.gov/neo/rest/v1/feed'

# --- USGS API Ayarları ---
# USGS API için anahtar gerekmez.
USGS_API_URL = 'https://earthquake.usgs.gov/fdsnws/event/1/query'


def fetch_nasa_neo_data(api_key):
    """
    NASA NeoWs (Near-Earth Object Web Service) API'sinden son 7 güne ait verileri çeker.
    Verileri bir JSON dosyasına kaydeder.
    """
    print("🛰️  NASA NEO verileri çekiliyor...")
    
    # Bugünün ve 7 gün öncesinin tarihlerini alalım
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': api_key
    }
    
    try:
        response = requests.get(NASA_API_URL, params=params)
        # HTTP 200 (OK) durum kodu geldiyse devam et
        response.raise_for_status() 
        
        data = response.json()
        
        # Veriyi JSON dosyasına düzgün formatta kaydet
        file_name = f"nasa_neo_data_{start_date}_to_{end_date}.json"
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"✅ Başarılı! NASA NEO verileri '{file_name}' dosyasına kaydedildi.")
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP Hatası Oluştu: {http_err} - Sunucu yanıtı: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"❌ İstek Hatası Oluştu: {req_err}")
    except json.JSONDecodeError:
        print("❌ JSON Verisi Çözümlenirken Hata Oluştu. Gelen yanıt JSON formatında olmayabilir.")
    return None


def fetch_usgs_earthquake_data():
    """
    USGS Deprem Kataloğu API'sinden son 30 güne ait 4.5 büyüklüğünden büyük depremleri çeker.
    Verileri bir JSON dosyasına kaydeder.
    """
    print("\n🌍 USGS Deprem verileri çekiliyor...")
    
    # Son 30 günün verilerini alalım
    end_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    start_time = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S')
    
    params = {
        'format': 'geojson',
        'starttime': start_time,
        'endtime': end_time,
        'minmagnitude': 4.5 # Sadece belirli bir büyüklükten büyük depremleri alalım
    }
    
    try:
        response = requests.get(USGS_API_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        file_name = "usgs_earthquake_data.json"
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"✅ Başarılı! USGS Deprem verileri '{file_name}' dosyasına kaydedildi.")
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP Hatası Oluştu: {http_err} - Sunucu yanıtı: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"❌ İstek Hatası Oluştu: {req_err}")
    except json.JSONDecodeError:
        print("❌ JSON Verisi Çözümlenirken Hata Oluştu.")
    return None


# --- Ana Kod Bloğu ---
if __name__ == "__main__":
    print("--- Veri Çekme İşlemi Başlatıldı ---")
    
    # NASA verilerini çek
    nasa_data = fetch_nasa_neo_data(NASA_API_KEY)
    
    # USGS verilerini çek
    usgs_data = fetch_usgs_earthquake_data()
    
    print("\n--- Veri Çekme İşlemi Tamamlandı ---")
    
    if nasa_data:
        print(f"Toplam {nasa_data.get('element_count', 0)} adet Dünya'ya yakın nesne verisi alındı.")
    
    if usgs_data:
        print(f"Toplam {len(usgs_data.get('features', []))} adet deprem verisi alındı.")