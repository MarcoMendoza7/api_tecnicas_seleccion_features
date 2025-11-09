# core/urls.py

from django.contrib import admin
from django.urls import path, include
# Importamos la vista del frontend (que crearemos)
from api.views_frontend import index 

urlpatterns = [
    # 1. RUTA RAÍZ: Servirá templates/index.html
    path('', index, name='index'), 
    
    path('admin/', admin.site.urls),
    
    # 2. RUTA API: Manejará la lógica de POST / Random Forest
    path('api/v1/', include('api.urls')),
]