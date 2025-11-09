# api/views_frontend.py

from django.shortcuts import render

def index(request):
    """Renderiza el index.html como página de inicio (ruta /)."""
    return render(request, 'index.html')