import numpy as np
import math
import json

# ==============================================================================
# 1. TEMEL FONKSİYON: Deprem büyüklüğünden yarıçap hesaplar. (Değişiklik yok)
# ==============================================================================
def calculate_impact_radii_from_magnitude(magnitude):
    """
    Verilen deprem büyüklüğüne göre potansiyel sismik etki yarıçaplarını (km cinsinden) hesaplar.
    """
    if magnitude is None or magnitude < 3.5:
        return {"yikici_sarsinti_yaricapi_km": 0, "orta_siddetli_sarsinti_yaricapi_km": 0, "hafif_sarsinti_yaricapi_km": 0}
    
    severe_radius_km = max(0, 2 * np.exp(magnitude - 5.5)) if magnitude > 4.5 else 0
    moderate_radius_km = max(0, 15 * np.exp(magnitude - 5.0)) if magnitude > 4.5 else 0
    light_radius_km = max(0, 50 * np.exp(magnitude - 4.5)) if magnitude > 3.5 else 0

    return {
        "yikici_sarsinti_yaricapi_km": round(severe_radius_km, 2),
        "orta_siddetli_sarsinti_yaricapi_km": round(moderate_radius_km, 2),
        "hafif_sarsinti_yaricapi_km": round(light_radius_km, 2)
    }

# ==============================================================================
# 2. GÜNCELLENMİŞ ANA FONKSİYON: Mutlak Parlaklık (H) ile etkiyi hesaplar.
# ==============================================================================
def calculate_asteroid_impact_effects(absolute_magnitude_h, density_kg_m3, velocity_kms, albedo=0.15):
    """
    Asteroidin mutlak parlaklığını (H), yoğunluğunu ve hızını kullanarak sismik etkiyi hesaplar.

    Args:
        absolute_magnitude_h (float): Asteroidin mutlak parlaklığı (H).
        density_kg_m3 (float): Asteroidin yoğunluğu (kg/m³).
        velocity_kms (float): Asteroidin hızı (km/s).
        albedo (float, optional): Asteroidin geometrik albedosu. Varsayılan değer 0.15'tir.
    """
    # Adım 1: Mutlak Parlaklık (H) ve Albedo'dan Çapı Hesapla
    # Formül: D (km) = (1329 / sqrt(albedo)) * 10^(-0.2 * H)
    diameter_km = (1329 / math.sqrt(albedo)) * (10**(-0.2 * absolute_magnitude_h))
    diameter_m = diameter_km * 1000 # Çapı metreye çevir

    # Adım 2: Kütleyi Hesapla
    radius_m = diameter_m / 2
    volume_m3 = (4/3) * math.pi * (radius_m ** 3)
    mass_kg = volume_m3 * density_kg_m3

    # Adım 3: Kinetik Enerjiyi Hesapla
    velocity_ms = velocity_kms * 1000
    kinetic_energy_joules = 0.5 * mass_kg * (velocity_ms ** 2)

    # Adım 4: Enerjiyi Eşdeğer Deprem Büyüklüğüne Çevir
    if kinetic_energy_joules > 0:
        equivalent_magnitude = (2/3) * math.log10(kinetic_energy_joules) - 6.07
    else:
        equivalent_magnitude = 0

    # Adım 5: Büyüklüğe Göre Etki Yarıçaplarını Hesapla
    impact_radii = calculate_impact_radii_from_magnitude(equivalent_magnitude)

    results = {
        "girilen_parametreler": {
            "mutlak_parlaklik_H": absolute_magnitude_h,
            "yogunluk_kg_m3": density_kg_m3,
            "hiz_kms": velocity_kms,
            "varsayilan_albedo": albedo
        },
        "hesaplanan_degerler": {
            "tahmini_cap_metre": f"{diameter_m:,.2f}",
            "tahmini_kutle_kg": f"{mass_kg:,.2f}",
            "kinetik_enerji_joule": f"{kinetic_energy_joules:,.2e}", # Bilimsel gösterimle daha okunaklı
            "esdeger_deprem_buyuklugu_Mw": round(equivalent_magnitude, 2)
        },
        "sismik_etki_yaricaplari_km": impact_radii
    }
    return results

# ==============================================================================
# --- GÜNCELLENMİŞ ÖRNEK KULLANIM ---
# ==============================================================================
if __name__ == "__main__":
    
    # Senaryo 1: Küçük ama parlak bir meteor (Chelyabinsk, H≈26.5)
    print("--- Senaryo 1: Küçük Meteor (H = 26.5) ---")
    small_impact = calculate_asteroid_impact_effects(
        absolute_magnitude_h=50.0,  # Parlaklık (daha büyük H = daha sönük/küçük cisim)
        density_kg_m3=3000,
        velocity_kms=100
    )
    print(json.dumps(small_impact, indent=4, ensure_ascii=False))
    
    # # Senaryo 2: Orta boy bir "şehir yok edici" asteroid (H≈22)
    # print("\n--- Senaryo 2: Orta Boy Meteor (H = 22) ---")
    # medium_impact = calculate_asteroid_impact_effects(
    #     absolute_magnitude_h=22,
    #     density_kg_m3=3000,
    #     velocity_kms=6.5
    # )
    # print(json.dumps(medium_impact, indent=4, ensure_ascii=False))

    # # Senaryo 3: Büyük, tehlikeli bir asteroid (H≈18)
    # print("\n--- Senaryo 3: Büyük Meteor (H = 18) ---")
    # large_impact = calculate_asteroid_impact_effects(
    #     absolute_magnitude_h=18,
    #     density_kg_m3=3000,
    #     velocity_kms=10
    # )
    # print(json.dumps(large_impact, indent=4, ensure_ascii=False))