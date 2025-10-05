import numpy as np
import math
import json

# ==============================================================================
# 1. BASE FUNCTION: Calculates seismic effect radii from earthquake magnitude.
# ==============================================================================
def calculate_impact_radii_from_magnitude(magnitude):
    """
    Given an equivalent earthquake magnitude, estimates the potential
    seismic effect radii in kilometers (for severe, moderate, and light shaking).
    """
    if magnitude is None or magnitude < 3.5:
        return {"yikici_sarsinti_yaricapi_km": 0, "orta_siddetli_sarsinti_yaricapi_km": 0, "hafif_sarsinti_yaricapi_km": 0}
    
    severe_radius_km = max(0, 2 * np.exp(magnitude - 5.5)) if magnitude > 4.5 else 0
    moderate_radius_km = max(0, 15 * np.exp(magnitude - 5.0)) if magnitude > 4.5 else 0
    light_radius_km = max(0, 50 * np.exp(magnitude - 4.5)) if magnitude > 3.5 else 0

    return {
        "yikici_sarsinti_yaricapi_km": round(severe_radius_km, 2),    # destructive shaking
        "orta_siddetli_sarsinti_yaricapi_km": round(moderate_radius_km, 2),  # moderate shaking
        "hafif_sarsinti_yaricapi_km": round(light_radius_km, 2)       # light shaking
    }

# ==============================================================================
# 2. NEW: Mass estimation from absolute magnitude
# ==============================================================================
def mass_from_absolute_magnitude(absolute_magnitude_h, density_kg_m3, albedo=0.15):
    """
    Estimate asteroid mass from absolute magnitude (H).

    Steps:
        1. Use H and albedo to estimate diameter (IAU standard formula).
        2. Convert diameter to volume (assuming spherical shape).
        3. Multiply volume by density to get mass.
    """
    # Step 1: Diameter from H and albedo (km → m)
    diameter_km = (1329 / math.sqrt(albedo)) * (10**(-0.2 * absolute_magnitude_h))
    diameter_m = diameter_km * 1000
    
    # Step 2: Volume (sphere approximation)
    radius_m = diameter_m / 2
    volume_m3 = (4/3) * math.pi * (radius_m ** 3)
    
    # Step 3: Mass
    mass_kg = volume_m3 * density_kg_m3
    
    return mass_kg, diameter_m

# ==============================================================================
# 3. MAIN FUNCTION: Now uses mass derived from brightness
# ==============================================================================
def calculate_asteroid_impact_effects(absolute_magnitude_h, density_kg_m3, velocity_kms, albedo=0.15):
    """
    Full asteroid impact model:
        1. Convert brightness (H) → mass.
        2. Calculate kinetic energy from mass & velocity.
        3. Convert kinetic energy → equivalent earthquake magnitude.
        4. Estimate seismic shaking radii.
    """
    # Step 1: Mass & diameter
    mass_kg, diameter_m = mass_from_absolute_magnitude(absolute_magnitude_h, density_kg_m3, albedo)

    # Step 2: Kinetic Energy
    velocity_ms = velocity_kms * 1000
    kinetic_energy_joules = 0.5 * mass_kg * (velocity_ms ** 2)

    # Step 3: Energy → Earthquake magnitude (empirical scaling)
    if kinetic_energy_joules > 0:
        equivalent_magnitude = (2/3) * math.log10(kinetic_energy_joules) - 6.07
    else:
        equivalent_magnitude = 0

    # Step 4: Effect radii
    impact_radii = calculate_impact_radii_from_magnitude(equivalent_magnitude)

    results = {
        "input_parameters": {
            "absolute_magnitude_H": absolute_magnitude_h,
            "density_kg_m3": density_kg_m3,
            "velocity_kms": velocity_kms,
            "assumed_albedo": albedo
        },
        "calculated_values": {
            "estimated_diameter_m": f"{diameter_m:,.2f}",
            "estimated_mass_kg": f"{mass_kg:,.2f}",
            "kinetic_energy_joules": f"{kinetic_energy_joules:,.2e}",
            "equivalent_earthquake_Mw": round(equivalent_magnitude, 2)
        },
        "seismic_effect_radii_km": impact_radii
    }
    return results

# ==============================================================================
# --- EXAMPLE USAGE ---
# ==============================================================================
if __name__ == "__main__":
    print("--- Scenario 1: Small Meteor (H = 30) ---")
    small_impact = calculate_asteroid_impact_effects(
        absolute_magnitude_h=30,
        density_kg_m3=3000,
        velocity_kms=180
    )
    print(json.dumps(small_impact, indent=4, ensure_ascii=False))
