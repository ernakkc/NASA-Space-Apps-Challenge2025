import requests
import json
import csv
import time

# NASA API anahtarını ve browse endpoint'ini tanımla
API_KEY = "1XfgKorYScmC6NcS1qA8RofukL9Ojj03syubqVfX"
BROWSE_URL = "https://api.nasa.gov/neo/rest/v1/neo/browse"

def fetch_all_neos():
    """
    NASA API'sinin /browse endpoint'ini kullanarak tüm NEO verilerini sayfa sayfa çeker.
    """
    all_neos = []
    page = 0
    total_pages = None

    while True:
        # API isteği için parametreleri oluştur
        params = {
            "page": page,
            "size": 20,  # Bir sayfada kaç asteroid olacağı (maksimum 20)
            "api_key": API_KEY
        }

        # İlerleme durumunu kullanıcıya bildir
        if total_pages:
            print(f"Sayfa {page + 1} / {total_pages} alınıyor...")
        else:
            print(f"Sayfa {page + 1} alınıyor...")

        try:
            # API'ye GET isteği gönder
            response = requests.get(BROWSE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            # Gelen asteroid verilerini ana listeye ekle
            if "near_earth_objects" in data:
                all_neos.extend(data["near_earth_objects"])

            # Toplam sayfa sayısını ilk istekte al
            if total_pages is None:
                total_pages = data.get("page", {}).get("total_pages", 0)
            
            # Son sayfaya ulaşıldıysa döngüden çık
            # API'nin sayfa numarası 0'dan başlar
            if page >= total_pages - 1:
                print("Tüm sayfalar başarıyla alındı!")
                break

            # Sonraki sayfaya geç
            page += 1
            
            # NASA'nın sunucusuna aşırı yüklenmemek ve rate limit'e takılmamak için
            # her istek arasında 1 saniye bekle.
            time.sleep(1)

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP Hatası Oluştu: {http_err} - Sunucudan gelen yanıt: {response.text}")
            break
        except requests.exceptions.RequestException as err:
            print(f"Bir Hata Oluştu: {err}")
            break

    return all_neos

def save_to_json(data, filename="all_asteroids.json"):
    """Veriyi JSON dosyasına kaydeder."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Veriler başarıyla '{filename}' dosyasına kaydedildi.")

def save_to_csv(data, filename="all_asteroids.csv"):
    """Veriyi CSV dosyasına kaydeder. Sadece belirli alanlar seçilir."""
    if not data:
        return

    # CSV'nin başlıklarını (sütun isimlerini) tanımla
    fieldnames = [
        'id', 'name', 'is_potentially_hazardous_asteroid', 
        'estimated_diameter_km_min', 'estimated_diameter_km_max',
        'first_observation_date', 'last_observation_date'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for neo in data:
            writer.writerow({
                'id': neo.get('id'),
                'name': neo.get('name'),
                'is_potentially_hazardous_asteroid': neo.get('is_potentially_hazardous_asteroid'),
                'estimated_diameter_km_min': neo.get('estimated_diameter', {}).get('kilometers', {}).get('estimated_diameter_min'),
                'estimated_diameter_km_max': neo.get('estimated_diameter', {}).get('kilometers', {}).get('estimated_diameter_max'),
                'first_observation_date': neo.get('orbital_data', {}).get('first_observation_date'),
                'last_observation_date': neo.get('orbital_data', {}).get('last_observation_date')
            })
            
    print(f"Veriler başarıyla '{filename}' dosyasına kaydedildi.")


if __name__ == "__main__":
    print("Tüm asteroid verileri çekilmeye başlanıyor. Bu işlem uzun sürebilir...")
    all_asteroid_data = fetch_all_neos()
    
    if all_asteroid_data:
        print(f"Toplam {len(all_asteroid_data)} adet asteroid verisi çekildi.")
        save_to_json(all_asteroid_data)
        save_to_csv(all_asteroid_data)
    else:
        print("Veri çekilemedi.")