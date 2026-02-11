from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('setup/', views.quiz_setup, name='quiz_setup'),
    path('take/', views.quiz_take, name='quiz_take'),
    path('history/', views.quiz_history, name='quiz_history'),
    path('generate-audio/', views.generate_audio, name='generate_audio'),
    path('export-flashcards/<int:quiz_id>/', views.export_flashcards, name='export_flashcards'),
]

