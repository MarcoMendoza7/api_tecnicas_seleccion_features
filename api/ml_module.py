# api/ml_module.py

import os
import io
import json
import pandas as pd
import base64
import gzip
import pickle
# Importaciones de Google Cloud
from google.cloud import storage 
from google.oauth2 import service_account

# Importaciones de Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

# --- Configuración del Dataset ---
TARGET_LABEL = 'calss' 
GCS_OBJECT_NAME = 'TotalFeatures-ISCXFlowMeter' 


# --- Funciones Auxiliares (Particionado y Eliminación de Etiquetas) ---

def train_val_test_split(df, train_percentage, rstate=42, shuffle=True, stratify=None):
    """
    Divide el DataFrame en conjuntos de entrenamiento, validación y prueba
    basándose en el porcentaje de entrenamiento proporcionado.
    """
    
    test_val_size = 1.0 - (train_percentage / 100.0) 
    val_test_size = 0.5 # 50% del conjunto restante para validación, 50% para prueba

    strat = df[stratify] if stratify else None
    
    # Primer split: Entrenamiento vs (Validación + Prueba)
    train_set, temp_set = train_test_split(
        df, test_size=test_val_size, random_state=rstate, shuffle=shuffle, stratify=strat)
    
    # Segundo split: Validación vs Prueba (50% de temp_set)
    strat_temp = temp_set[stratify] if stratify else None
    val_set, test_set = train_test_split(
        temp_set, test_size=val_test_size, random_state=rstate, shuffle=shuffle, stratify=strat_temp)
    
    return (train_set, val_set, test_set)


def remove_labels(df, label_name): 
    """Separa el DataFrame en características (X) y etiquetas (y)."""
    X = df.drop(label_name, axis=1, errors='ignore')
    y = df[label_name].copy()
    return (X, y)


# --- Funciones de Carga de Datos (GCS) ---

def load_data_from_gcs():
    """Carga el dataset comprimido (.pkl.gz) desde Google Cloud Storage."""
    try:
        credentials_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
        bucket_name = os.environ.get('GCS_BUCKET_NAME')
        object_name = os.environ.get('GCS_OBJECT_NAME') # Usaremos esta variable
        
        if not all([credentials_json, bucket_name, object_name]):
            raise ValueError("Variables de GCS incompletas.")

        # 1. Autenticación (mismo código corregido)
        credentials_info = json.loads(credentials_json)
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info
        )
        client = storage.Client(credentials=credentials)
        bucket = client.bucket(bucket_name) 
        blob = bucket.blob(object_name) # Usando el nombre del archivo PKL.GZ

        print(f"DEBUG: Intentando descargar {object_name}...")
        
        # 2. Descargar como bytes
        data_bytes = blob.download_as_bytes()
        
        # 3. Leer el .pkl.gz directamente desde los bytes en memoria.
        # Esto es muy eficiente porque Pandas maneja la descompresión gzip internamente.
        df = pd.read_pickle(io.BytesIO(data_bytes), compression='gzip')
        
        print(f"DEBUG: Dataset cargado exitosamente. Filas: {len(df)}")
        return df

    except Exception as e:
        print(f"Error al cargar el dataset de GCS: {e}")
        # Si tienes problemas, el error 403 puede ser por la facturación (de nuevo)
        return None


# --- Función Principal de la API ---

def run_feature_selection(train_percentage):
    """
    Ejecuta el proceso completo de Random Forest, selección de características
    y cálculo de métricas en función del porcentaje de entrenamiento.
    """
    df = load_data_from_gcs()
    if df is None:
        # Este mensaje es el que devolverá el Error 500
        return {"error": "Error 500: No se pudo cargar el dataset de GCS. Revisa tus credenciales y nombre del bucket."}
    
    # 1. Partición del DataSet usando el porcentaje del usuario
    try:
        train_set, val_set, test_set = train_val_test_split(
            df, 
            train_percentage=train_percentage, 
            stratify=TARGET_LABEL 
        )
    except Exception as e:
        return {"error": f"Error 500: Error al particionar el dataset. {e}"}

    # Separar X (features) y y (labels)
    X_train, y_train = remove_labels(train_set, TARGET_LABEL)
    X_val, y_val = remove_labels(val_set, TARGET_LABEL)
    
    # 2. Entrenar el Random Forest (Modelo Inicial)
    clf_rnd_initial = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
    clf_rnd_initial.fit(X_train, y_train)

    # 3. Cálculo de la Importancia de las Características
    feature_importances = pd.Series(
        clf_rnd_initial.feature_importances_, 
        index=X_train.columns
    )
    
    # 4. Obtener Resultados Solicitados
    
    # 4.1. Características en orden ascendente (menos importantes primero)
    features_asc = feature_importances.sort_values(ascending=True).index.tolist()
    
    # 4.2. 10 características más relevantes (descendente)
    top_10_features_desc = feature_importances.sort_values(ascending=False).head(10).index.tolist()
    
    # 4.3. Predecir y calcular F1 Score del set de validación (Modelo Inicial)
    y_val_pred_initial = clf_rnd_initial.predict(X_val)
    f1_val_initial = f1_score(y_val, y_val_pred_initial, average='weighted')

    # 4.4. Predecir y calcular F1 Score del set de entrenamiento (Modelo Inicial)
    y_train_pred_initial = clf_rnd_initial.predict(X_train)
    f1_train_initial = f1_score(y_train, y_train_pred_initial, average='weighted')

    # 5. Opcional: Reentrenamiento con el modelo reducido (por tu Notebook)
    X_train_reduced = X_train[top_10_features_desc].copy()
    X_val_reduced = X_val[top_10_features_desc].copy()
    
    clf_rnd_reduced = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
    clf_rnd_reduced.fit(X_train_reduced, y_train)

    # F1 Score del set de validación (Modelo Reducido)
    y_val_pred_reduced = clf_rnd_reduced.predict(X_val_reduced)
    f1_val_reduced = f1_score(y_val, y_val_pred_reduced, average='weighted')
    
    # F1 Score del set de entrenamiento (Modelo Reducido)
    y_train_pred_reduced = clf_rnd_reduced.predict(X_train_reduced)
    f1_train_reduced = f1_score(y_train, y_train_pred_reduced, average='weighted')

    return {
        # Resultados Solicitados (del Modelo Inicial)
        "f1_score_validation": round(f1_val_initial, 4),
        "f1_score_training": round(f1_train_initial, 4),
        "features_asc": features_asc,
        "top_10_features_desc": top_10_features_desc,
        
        # Resultados del Modelo Reducido (Extra)
        "f1_score_validation_reduced": round(f1_val_reduced, 4),
        "f1_score_training_reduced": round(f1_train_reduced, 4),
        
        # Metadatos
        "train_size": len(X_train),
        "validation_size": len(X_val),
    }