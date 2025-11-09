# api/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt # <-- Importación añadida
from .ml_module import run_feature_selection
import os
from pymongo import MongoClient
import datetime
# Eliminadas las importaciones de 'json' y 'method_decorator' que no se usaban

# --- Función para guardar el log ---
def save_analysis_log(train_percentage, results):
    try:
        MONGO_URI = os.environ.get('MONGO_URI')
        if not MONGO_URI:
            print("WARNING: MONGO_URI no está configurada. El log no se guardará.")
            return

        client = MongoClient(MONGO_URI)
        db = client['feature_selection_db']
        collection = db['analysis_logs']
        
        # Construir el documento de log
        log_document = {
            "timestamp": datetime.datetime.now(),
            "train_percentage": train_percentage,
            "results_summary": {
                "f1_validation": results.get('f1_score_validation'),
                "top_10_features": results.get('top_10_features_desc'),
            },
            "full_results": results
        }
        
        collection.insert_one(log_document)
        client.close()
        
    except Exception as e:
        print(f"Error al guardar log en MongoDB: {e}")


@csrf_exempt # <------------------------------------------- ¡DESHABILITAR CSRF!
@api_view(['POST'])
def feature_selection_api(request):
    """
    Endpoint principal para ejecutar la selección de características y guardar el log.
    """
    # 1. Obtener y validar el porcentaje
    try:
        train_percentage = request.data.get('train_percentage')
        if train_percentage is None:
            return Response({"error": "Debe proporcionar 'train_percentage'."}, status=400)
        
        train_percentage = float(train_percentage)
        if not (1 <= train_percentage <= 100):
            return Response({"error": "El porcentaje debe estar entre 1 y 100."}, status=400)

    except ValueError:
        return Response({"error": "El porcentaje de entrenamiento debe ser un número."}, status=400)

    # 2. Ejecutar la lógica de ML
    results = run_feature_selection(train_percentage)

    # 3. Manejar errores del módulo ML (e.g., Error de GCS)
    if "error" in results:
        return Response(results, status=500)

    # 4. REGISTRO EN MONGODB
    save_analysis_log(train_percentage, results)
    
    # 5. Devolver la respuesta al cliente
    return Response({
        "message": "Análisis de características completado.",
        "input_percentage": train_percentage,
        "results": results
    })