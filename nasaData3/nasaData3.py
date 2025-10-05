# --- BU KODUN TAMAMINI KOPYALAYIN ---
import requests
import json
import os

# JPL Small-Body Database API'sinin adresi
api_url = "https://ssd-api.pl.nasa.gov/sbdb.api"

# Sorgulamak istediğimiz asteroidin adı veya numarası
asteroid_adi = "433 Eros"

# Kaydedilecek dosyanın adını asteroid adına göre oluşturalım
dosya_adi = f"{asteroid_adi.replace(' ', '_')}_data.json"

# API'ye göndereceğimiz DOĞRU parametreler
params = {
    "sstr": asteroid_adi,
    "orb-elem": "1",  # 'orb' DEĞİL, 'orb-elem' olmalı
    "phys-par": "1"   # 'phys' DEĞİL, 'phys-par' olmalı
}

print(f"'{asteroid_adi}' için veriler JPL SBDB API'sinden alınıyor...")

try:
    # API'ye GET isteği gönderiyoruz
    response = requests.get(api_url, params=params)

    # İsteğin başarılı olup olmadığını kontrol ediyoruz
    if response.status_code == 200:
        data = response.json()
        
        # Dosyaya yazma
        with open(dosya_adi, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("\n----- Veri Başarıyla Alındı! -----")
        print(f"Tüm veriler '{os.path.abspath(dosya_adi)}' dosyasına kaydedildi.")

    else:
        print(f"Hata! Sunucudan gelen durum kodu: {response.status_code}")
        print(f"Hata Mesajı: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Bir bağlantı hatası oluştu: {e}")