import numpy as np
import math
import json

# ==============================================================================
# 1. TEMEL FONKSİYON: Deprem büyüklüğünden yarıçap hesaplar. (Değişiklik yok)
# ==============================================================================
def calculate_impact_radii_from_magnitude(magnitude):
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
# 2. YENİ: Parlaklıktan kütle hesabı
# ==============================================================================
def mass_from_absolute_magnitude(absolute_magnitude_h, density_kg_m3, albedo=0.15):
    """
    Mutlak parlaklıktan (H) asteroid kütlesini tahmin eder.
    1. H + albedo -> çap
    2. Çap -> hacim
    3. Hacim * yoğunluk -> kütle
    """
    # H ve albedodan çap (km)
    diameter_km = (1329 / math.sqrt(albedo)) * (10**(-0.2 * absolute_magnitude_h))
    diameter_m = diameter_km * 1000
    
    # Hacim
    radius_m = diameter_m / 2
    volume_m3 = (4/3) * math.pi * (radius_m ** 3)
    
    # Kütle
    mass_kg = volume_m3 * density_kg_m3
    
    return mass_kg, diameter_m

# ==============================================================================
# 3. ANA FONKSİYON: Artık direkt kütleyi kullanıyor
# ==============================================================================
def calculate_asteroid_impact_effects(absolute_magnitude_h, density_kg_m3, velocity_kms, albedo=0.15):
    """
    Parlaklıktan önce kütle tahmini yapar, sonra etki hesaplar.
    """
    # Adım 1: Kütleyi ve çapı hesapla
    mass_kg, diameter_m = mass_from_absolute_magnitude(absolute_magnitude_h, density_kg_m3, albedo)

    # Adım 2: Kinetik Enerji
    velocity_ms = velocity_kms * 1000
    kinetic_energy_joules = 0.5 * mass_kg * (velocity_ms ** 2)

    # Adım 3: Eşdeğer deprem büyüklüğü
    if kinetic_energy_joules > 0:
        equivalent_magnitude = (2/3) * math.log10(kinetic_energy_joules) - 6.07
    else:
        equivalent_magnitude = 0

    # Adım 4: Etki yarıçapları
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
            "kinetik_enerji_joule": f"{kinetic_energy_joules:,.2e}",
            "esdeger_deprem_buyuklugu_Mw": round(equivalent_magnitude, 2)
        },
        "sismik_etki_yaricaplari_km": impact_radii
    }
    return results

# ==============================================================================
# --- ÖRNEK KULLANIM ---
# ==============================================================================
if __name__ == "__main__":
    print("--- Senaryo 1: Küçük Meteor (H = 26.5) ---")
    small_impact = calculate_asteroid_impact_effects(
        absolute_magnitude_h=30,
        density_kg_m3=3000,
        velocity_kms=180
    )
    print(json.dumps(small_impact, indent=4, ensure_ascii=False))
