import pandas as pd

csv_path = "/home/marco/Documentos/api_tecnicas_seleccion/TotalFeatures-ISCXFlowMeter.csv"
df = pd.read_csv(csv_path)

pkl_path = "/home/marco/Documentos/api_tecnicas_seleccion/TotalFeatures-ISCXFlowMeter.pkl"
df.to_pickle(pkl_path)

print("Conversión completa. Archivo guardado como .pkl :)")

import pandas as pd
df = pd.read_pickle("/home/marco/Documentos/datasets/TotalFeatures-ISCXFlowMeter.pkl")
print(df.head())
