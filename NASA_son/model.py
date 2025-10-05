import json
import pandas as pd
import numpy as np
import glob  # Dosya yollarını bulmak için

# Makine Öğrenmesi Kütüphaneleri
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score

# Görselleştirme Kütüphaneleri
import matplotlib.pyplot as plt
import seaborn as sns

print("Gerekli kütüphaneler başarıyla yüklendi.")


def process_nasa_data_to_dataframe(file_path):
    """
    NASA'dan çekilen ham JSON verisini işler ve temiz bir Pandas DataFrame'e dönüştürür.
    Bu sürüm, 'orbital_data'nın eksik olmasını tolere eder.
    """
    print(f"'{file_path}' dosyasından veriler okunuyor ve işleniyor...")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    processed_asteroids = []

    for date in data['near_earth_objects']:
        for asteroid in data['near_earth_objects'][date]:
            try:
                # Orbital veriyi güvenli bir şekilde al, yoksa boş bir sözlük ata
                orbital_data = asteroid.get('orbital_data', {})

                asteroid_info = {
                    'id': asteroid.get('id'),
                    'name': asteroid.get('name'),
                    'is_potentially_hazardous_asteroid': int(asteroid.get('is_potentially_hazardous_asteroid', 0)),
                    'absolute_magnitude_h': asteroid.get('absolute_magnitude_h'),
                    'est_diameter_min_km': asteroid['estimated_diameter']['kilometers'].get('estimated_diameter_min'),
                    'est_diameter_max_km': asteroid['estimated_diameter']['kilometers'].get('estimated_diameter_max'),
                    'relative_velocity_kps': float(asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_second']),
                    'miss_distance_km': float(asteroid['close_approach_data'][0]['miss_distance']['kilometers']),
                    
                    # Orbital verileri .get() ile güvenli bir şekilde al, yoksa None ata
                    'eccentricity': orbital_data.get('eccentricity'),
                    'semi_major_axis': orbital_data.get('semi_major_axis'),
                    'inclination': orbital_data.get('inclination'),
                    'orbital_period': orbital_data.get('orbital_period'),
                    'perihelion_distance': orbital_data.get('perihelion_distance'),
                    'aphelion_distance': orbital_data.get('aphelion_distance'),
                }
                # Verileri float'a dönüştürmeyi dene, olmazsa None olarak kalsın
                for key in ['eccentricity', 'semi_major_axis', 'inclination', 'orbital_period', 'perihelion_distance', 'aphelion_distance']:
                    if asteroid_info[key] is not None:
                        asteroid_info[key] = float(asteroid_info[key])

                processed_asteroids.append(asteroid_info)
            except (KeyError, IndexError, TypeError) as e:
                # Bu blok, çap veya hız gibi daha temel veriler eksikse çalışır
                print(f"Uyarı: Bir kayıt işlenemedi. Hata: {e}")
                pass

    df = pd.DataFrame(processed_asteroids)
    print(f"Veriler başarıyla DataFrame'e dönüştürüldü. Toplam {len(df)} kayıt okundu.")
    return df


def feature_engineering(df):
    """
    DataFrame üzerinde yeni ve anlamlı özellikler türetir (Özellik Mühendisliği).
    """
    print("Özellik mühendisliği uygulanıyor...")

    df['est_diameter_mean_km'] = (df['est_diameter_min_km'] + df['est_diameter_max_km']) / 2
    df['kinetic_energy_proxy'] = (df['est_diameter_mean_km'] ** 3) * (df['relative_velocity_kps'] ** 2)
    
    # Eccentricity verisi varsa 'orbit_stability' özelliğini oluştur
    if 'eccentricity' in df.columns and df['eccentricity'].notna().any():
        df['orbit_stability'] = 1 - df['eccentricity']
    
    epsilon = 1e-6
    df['threat_score'] = df['kinetic_energy_proxy'] / (df['miss_distance_km'] + epsilon)

    print("Yeni özellikler oluşturuldu.")
    return df


def visualize_feature_importance(model, features):
    """
    Eğitilmiş modelin özellik önemlerini görselleştirir.
    """
    feature_imp = pd.DataFrame(sorted(zip(model.feature_importances_, features)), columns=['Value', 'Feature'])

    plt.figure(figsize=(12, 8))
    sns.barplot(x="Value", y="Feature", data=feature_imp.sort_values(by="Value", ascending=False))
    plt.title('LightGBM Özellik Önemleri')
    plt.xlabel('Önem Skoru')
    plt.ylabel('Özellikler')
    plt.tight_layout()
    plt.show()


# --- ANA İŞLEM AKIŞI ---
if __name__ == "__main__":
    try:
        json_file = glob.glob("nasa_neo_data*.json")[0]
    except IndexError:
        print("❌ Hata: 'nasa_neo_data' ile başlayan bir JSON dosyası bulunamadı. Lütfen önce veri çekme kodunu çalıştırın.")
        exit()

    df = process_nasa_data_to_dataframe(json_file)

    if df.empty:
        print("❌ Hata: JSON dosyasından hiç veri okunamadı. Dosyanın yapısını kontrol edin.")
        exit()

    print("\nVeri temizliği yapılıyor...")
    print("Temizlik öncesi eksik veri durumu:")
    print(df.isnull().sum())

    # Model için KRİTİK olan sütunlarda eksik veri varsa o satırları sil.
    critical_cols = [
        'est_diameter_min_km', 'est_diameter_max_km', 'relative_velocity_kps',
        'miss_distance_km'
    ]
    df.dropna(subset=critical_cols, inplace=True)

    print(f"Kritik verileri eksik olan satırlar temizlendi. Kalan satır sayısı: {len(df)}")

    if df.empty:
        print("❌ Hata: Veri temizliği sonrası işlenecek veri kalmadı.")
        exit()

    df_featured = feature_engineering(df.copy())

    print("\nModel için veriler hazırlanıyor...")
    target_variable = 'is_potentially_hazardous_asteroid'
    y = df_featured[target_variable]

    features_to_drop = ['id', 'name', target_variable]
    X = df_featured.drop(columns=features_to_drop)
    
    # Eğer orbital verileri hiç gelmediyse bu sütunları da X'ten çıkar
    for col in ['eccentricity', 'semi_major_axis', 'inclination', 'orbital_period', 'perihelion_distance', 'aphelion_distance', 'orbit_stability']:
        if col in X.columns and X[col].isnull().all():
            X = X.drop(columns=[col])
            print(f"Uyarı: '{col}' sütunu tamamen boş olduğu için modelden çıkarıldı.")


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Veri seti ayrıldı: {len(X_train)} eğitim, {len(X_test)} test örneği.")

    print("\n--- LightGBM Modeli Eğitiliyor ---")
    lgbm = lgb.LGBMClassifier(objective='binary', is_unbalance=True, random_state=42)
    lgbm.fit(X_train, y_train)
    print("✅ Model başarıyla eğitildi.")

    print("\n--- Model Değerlendiriliyor ---")
    y_pred = lgbm.predict(X_test)
    y_pred_proba = lgbm.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Doğruluğu: {accuracy:.4f}")

    roc_auc = roc_auc_score(y_test, y_pred_proba)
    print(f"ROC AUC Skoru: {roc_auc:.4f}")

    print("\nSınıflandırma Raporu:")
    print(classification_report(y_test, y_pred, target_names=['Tehlikesiz (0)', 'Tehlikeli (1)']))

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Tehlikesiz', 'Tehlikeli'], yticklabels=['Tehlikesiz', 'Tehlikeli'])
    plt.xlabel('Tahmin Edilen Sınıf')
    plt.ylabel('Gerçek Sınıf')
    plt.title('Karmaşıklık Matrisi')
    plt.show()

    print("\n--- Özellik Önemleri Hesaplanıyor ---")
    visualize_feature_importance(lgbm, X.columns)