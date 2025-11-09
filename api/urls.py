# api/urls.py

from django.urls import path
from .views import feature_selection_api

urlpatterns = [
    # Endpoint: /api/v1/analyze/
    path('analyze/', feature_selection_api, name='feature_analysis'),
]