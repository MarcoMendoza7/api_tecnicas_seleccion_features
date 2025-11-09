import pandas as pd
import time
import os

# Ruta base (ajústala según tu caso)
csv_path = "/home/marco/Documentos/api_tecnicas_seleccion/TotalFeatures-ISCXFlowMeter.csv"
pkl_path = "/home/marco/Documentos/api_tecnicas_seleccion/TotalFeatures-ISCXFlowMeter.pkl"
pkl_gz_path = "/home/marco/Documentos/api_tecnicas_seleccion/TotalFeatures-ISCXFlowMeter.pkl.gz"

# 1️⃣ Cargar CSV
print("📂 Cargando dataset CSV...")
start = time.time()
df_csv = pd.read_csv(csv_path)
csv_time = time.time() - start
print(f"✅ CSV cargado en {csv_time:.2f} segundos.")

# Guardar en .pkl
print("\n💾 Guardando como PKL...")
df_csv.to_pickle(pkl_path)
pkl_size = os.path.getsize(pkl_path) / (1024 * 1024)
print(f"✅ PKL guardado ({pkl_size:.2f} MB)")

# Guardar en .pkl.gz (comprimido)
print("\n💾 Guardando como PKL.GZ (comprimido)...")
df_csv.to_pickle(pkl_gz_path, compression="gzip")
pkl_gz_size = os.path.getsize(pkl_gz_path) / (1024 * 1024)
print(f"✅ PKL.GZ guardado ({pkl_gz_size:.2f} MB)")

# 2️⃣ Probar tiempos de carga de cada formato
def medir_tiempo_carga(func, path, label):
    start = time.time()
    df = func(path)
    elapsed = time.time() - start
    print(f"⏱️ {label} cargado en {elapsed:.2f} segundos.")
    return df, elapsed

print("\n🚀 Midiendo tiempos de carga...")

df_pkl, pkl_time = medir_tiempo_carga(pd.read_pickle, pkl_path, ".PKL")
df_pkl_gz, pkl_gz_time = medir_tiempo_carga(lambda x: pd.read_pickle(x, compression='gzip'), pkl_gz_path, ".PKL.GZ")

# 3️⃣ Verificar que los datos sean idénticos
same_pkl = df_csv.equals(df_pkl)
same_pkl_gz = df_csv.equals(df_pkl_gz)

# 4️⃣ Mostrar resultados finales
print("\n📊 RESULTADOS FINALES:")
print(f"CSV size: {os.path.getsize(csv_path) / (1024 * 1024):.2f} MB")
print(f"PKL size: {pkl_size:.2f} MB")
print(f"PKL.GZ size: {pkl_gz_size:.2f} MB")
print(f"CSV load time: {csv_time:.2f} s")
print(f"PKL load time: {pkl_time:.2f} s")
print(f"PKL.GZ load time: {pkl_gz_time:.2f} s")
print(f"\n✅ Datos PKL iguales al CSV: {same_pkl}")
print(f"✅ Datos PKL.GZ iguales al CSV: {same_pkl_gz}")
