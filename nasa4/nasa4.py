import requests
import json
import sys

# SBDB API URL
SBDB_URL = "https://ssd-api.jpl.nasa.gov/sbdb.api"

def fetch_asteroid_data(designation, save_file="asteroid_data.json"):
    params = {
        "sstr": designation,
        "full-prec": "true",
        "phys-par": "true"
    }

    try:
        print(f"[+] {designation} için NASA SBDB API'den veri çekiliyor...")
        resp = requests.get(SBDB_URL, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()

        with open(save_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"[✓] Veri başarıyla kaydedildi: {save_file}")
        return data

    except requests.HTTPError as http_err:
        print(f"[!] HTTP hata: {http_err}")
        print("Response:", resp.text[:500])
    except Exception as e:
        print(f"[!] Hata: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        designation = sys.argv[1]
    else:
        designation = "433"  # Örnek asteroid (Eros)

    data = fetch_asteroid_data(designation)

    if data:
        print("\n=== Özet Bilgiler ===")
        obj = data.get("object", {})
        orbit = data.get("orbit", {})
        phys = data.get("phys_par", {})

        # Eğer phys listeyse ilk elemanı al
        if isinstance(phys, list) and len(phys) > 0:
            phys = phys[0]

        # Yörünge parametreleri elements listesi içinde
        a, e, inc = "bilgi yok", "bilgi yok", "bilgi yok"
        if "elements" in orbit:
            elements = orbit["elements"]
            for el in elements:
                if el.get("name") == "a":
                    a = el.get("value", "bilgi yok")
                if el.get("name") == "e":
                    e = el.get("value", "bilgi yok")
                if el.get("name") == "i":
                    inc = el.get("value", "bilgi yok")

        print("Ad:", obj.get("fullname", obj.get("des")))
        print("Çap:", phys.get("diameter", "bilgi yok"), "km")
        print("Yörünge yarı büyük eksen (a):", a)
        print("Eksantriklik (e):", e)
        print("Eğim (i):", inc)
