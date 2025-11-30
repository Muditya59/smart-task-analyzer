from django.urls import path
from . import views

urlpatterns = [
    # API endpoints for /api/tasks/analyze/ and /api/tasks/suggest/
    path('analyze/', views.analyze_tasks, name='analyze_tasks'),
    path('suggest/', views.suggest_tasks, name='suggest_tasks'),
]