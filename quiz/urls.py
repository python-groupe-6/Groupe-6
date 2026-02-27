from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('setup/', views.quiz_setup, name='quiz_setup'),
    path('take/', views.quiz_take, name='quiz_take'),
    path('take/<int:quiz_id>/', views.quiz_take, name='quiz_take_id'),
    path('history/', views.quiz_history, name='quiz_history'),
    path('generate-audio/', views.generate_audio, name='generate_audio'),
    path('export-flashcards/<int:quiz_id>/', views.export_flashcards, name='export_flashcards'),
    path('analysis/<int:history_id>/', views.quiz_analysis, name='quiz_analysis'),
    path('save-flashcard/', views.save_flashcard, name='save_flashcard'),
    path('srs/', views.srs_dashboard, name='srs_dashboard'),
    path('srs/review/', views.srs_review, name='srs_review'),
    path('ai-tutor-chat/', views.ai_tutor_chat, name='ai_tutor_chat'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('library/', views.public_library, name='public_library'),
    path('toggle-public/<int:quiz_id>/', views.toggle_public, name='toggle_public'),
    path('like-quiz/<int:quiz_id>/', views.like_quiz, name='like_quiz'),
]




