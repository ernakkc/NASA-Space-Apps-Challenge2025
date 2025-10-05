import json
import numpy as np

def calculate_impact_radii(magnitude):
    """
    Verilen deprem büyüklüğüne göre potansiyel etki yarıçaplarını (km cinsinden) hesaplar.
    Bu formüller basitleştirilmiş bir modeldir ve gerçek jeolojik koşullara göre değişebilir.
    """
    if magnitude is None:
        return {
            "yikici_sarsinti_yaricapi_km": 0,
            "orta_siddetli_sarsinti_yaricapi_km": 0,
            "hafif_sarsinti_yaricapi_km": 0
        }
        
    # Yüksek Şiddetli Sarsıntı (Potansiyel olarak yıkıcı)
    severe_radius_km = max(0, 2 * np.exp(magnitude - 5.5)) if magnitude > 5.5 else 0

    # Orta Şiddetli Sarsıntı (Eşyaları devirebilir, hafif hasar)
    moderate_radius_km = max(0, 15 * np.exp(magnitude - 5.0)) if magnitude > 4.5 else 0

    # Hafif Sarsıntı (Herkes tarafından hissedilir)
    light_radius_km = max(0, 50 * np.exp(magnitude - 4.5)) if magnitude > 3.5 else 0

    return {
        "yikici_sarsinti_yaricapi_km": round(severe_radius_km, 2),
        "orta_siddetli_sarsinti_yaricapi_km": round(moderate_radius_km, 2),
        "hafif_sarsinti_yaricapi_km": round(light_radius_km, 2)
    }

# --- ANA İŞLEM KISMI ---

# 1. JSON dosyasını oku
try:
    with open('usgs_earthquake_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Hata: usgs_earthquake_data.json dosyası bulunamadı. Dosyanın kodla aynı dizinde olduğundan emin olun.")
    exit()

# 2. JSON içindeki 'features' listesine eriş
earthquakes = data.get('features', [])

# 3. Her bir deprem verisi için döngü başlat ve bilgileri işle
for earthquake in earthquakes:
    properties = earthquake.get('properties', {})
    geometry = earthquake.get('geometry', {})

    # Gerekli bilgileri JSON'dan al
    magnitude = properties.get('mag')
    place = properties.get('place', 'Bilinmeyen yer')
    
    if geometry and 'coordinates' in geometry:
        coordinates = geometry['coordinates']
        longitude = coordinates[0]
        latitude = coordinates[1]
        depth = coordinates[2]
    else:
        longitude, latitude, depth = 'Bilinmiyor', 'Bilinmiyor', 'Bilinmiyor'

    # Etki yarıçaplarını hesapla
    impact_radii = calculate_impact_radii(magnitude)

    # Sonuçları ekrana yazdır
    print("-" * 50)
    print(f"Deprem Bilgisi: {place}")
    print(f"Büyüklük: {magnitude}")
    print(f"Konum (Enlem, Boylam): {latitude}, {longitude}")
    print(f"Derinlik: {depth} km")
    print("\nTahmini Etki Alanı Yarıçapları:")
    print(f"  - Yıkıcı Sarsıntı: {impact_radii['yikici_sarsinti_yaricapi_km']} km")
    print(f"  - Orta Şiddetli Sarsıntı: {impact_radii['orta_siddetli_sarsinti_yaricapi_km']} km")
    print(f"  - Hafif Sarsıntı: {impact_radii['hafif_sarsinti_yaricapi_km']} km\n")

print(f"Toplam {len(earthquakes)} adet deprem verisi işlendi.")