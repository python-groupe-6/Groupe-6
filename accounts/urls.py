from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('subscription/', views.subscription_view, name='subscription'),

    # Password Reset URLs (Custom SPA Flow)
    path('password-reset/', views.password_reset_spa, name='password_reset'),
    path('api/send-reset-code/', views.send_reset_code, name='send_reset_code'),
    path('api/verify-reset-code/', views.verify_reset_code, name='verify_reset_code'),
    path('api/reset-password/', views.reset_password_action, name='reset_password_action'),
]
