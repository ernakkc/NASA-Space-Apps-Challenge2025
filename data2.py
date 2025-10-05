import requests
import json

# NASA API anahtarını ve browse endpoint'ini tanımla
API_KEY = "1XfgKorYScmC6NcS1qA8RofukL9Ojj03syubqVfX"
BROWSE_URL = "https://api.nasa.gov/neo/rest/v1/feed"

def get_and_save_sample():
    """
    NASA API'sinden ilk 5 asteroidin verisini çeker ve bir JSON dosyasına kaydeder.
    """
    # API isteği için parametreleri oluştur
    params = {
        "page": 0,
        "size": 5, 
        "api_key": API_KEY
    }

    print("Veri örneği NASA'dan isteniyor...")

    try:
        # API'ye GET isteği gönder
        response = requests.get(BROWSE_URL, params=params)
        response.raise_for_status()  # İstek başarısız olursa hata fırlat
        
        # Gelen JSON verisini Python sözlüğüne çevir
        data = response.json()
        
        # Hedef dosya adını belirle
        filename = "asteroid_sample.json"
        
        # Veriyi dosyaya yaz
        with open(filename, 'w', encoding='utf-8') as f:
            # json.dump(), Python sözlüğünü dosyaya JSON formatında yazar
            # indent=4, dosyanın okunabilir (girintili) olmasını sağlar
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"\nİstek Başarılı! Veri örneği '{filename}' dosyasına kaydedildi.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Hatası Oluştu: {http_err} - Sunucudan gelen yanıt: {response.text}")
    except requests.exceptions.RequestException as err:
        print(f"Bir Hata Oluştu: {err}")

if __name__ == "__main__":
    get_and_save_sample()