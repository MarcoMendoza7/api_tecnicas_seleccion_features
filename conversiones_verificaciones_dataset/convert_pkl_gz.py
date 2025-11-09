import pandas as pd

# Cargar el CSV original
df = pd.read_csv("TotalFeatures-ISCXFlowMeter.csv")

# Guardar versión normal
df.to_pickle("TotalFeatures-ISCXFlowMeter.pkl")

# Guardar versión comprimida (sin perder datos)
df.to_pickle("TotalFeatures-ISCXFlowMeter.pkl.gz", compression="gzip")

# Leer versión comprimida (es igual)
df_loaded = pd.read_pickle("TotalFeatures-ISCXFlowMeter.pkl.gz", compression="gzip")

# Comprobar que sean iguales
print(df.equals(df_loaded))  # Esto debería imprimir True ✅
