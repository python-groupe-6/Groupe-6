from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, UserUpdateForm, SettingsUpdateForm
from django.utils import translation
from django.conf import settings

def register(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue, {user.username} ! Votre compte a été créé.")
            return redirect('core:home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

from django.db.models import Avg, Sum
from quiz.models import ScoreHistory

@login_required
def dashboard_view(request):
    user_scores = ScoreHistory.objects.filter(user=request.user)
    
    total_quizzes = user_scores.count()
    completed_quizzes = total_quizzes # Simplified for now
    
    avg_score_raw = user_scores.aggregate(Avg('score'))['score__avg'] or 0
    avg_total_raw = user_scores.aggregate(Avg('total_questions'))['total_questions__avg'] or 1
    
    # Calculate percentage
    if avg_total_raw > 0:
        average_score_pct = round((avg_score_raw / avg_total_raw) * 100)
    else:
        average_score_pct = 0
        
    stats = {
        'total_quizzes': total_quizzes,
        'completed_quizzes': completed_quizzes,
        'average_score': average_score_pct,
        'time_spent': 'Dépend du chrono'
    }
    return render(request, 'accounts/dashboard.html', {'stats': stats})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès !")
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def settings_view(request):
    form = SettingsUpdateForm(instance=request.user.profile)
    password_form = PasswordChangeForm(user=request.user)
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'preferences':
            form = SettingsUpdateForm(request.POST, instance=request.user.profile)
            if form.is_valid():
                profile = form.save()
                
                # Activate new language
                translation.activate(profile.language)
                request.session[translation.LANGUAGE_SESSION_KEY] = profile.language
                
                messages.success(request, "Vos préférences générales ont été mises à jour !")
                return redirect('accounts:settings')
        
        elif form_type == 'password_change':
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important to keep the user logged in
                messages.success(request, "Votre mot de passe a été modifié avec succès !")
                return redirect('accounts:settings')
            else:
                messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
                
        elif form_type == 'notifications':
            # Mock handling for notification preferences
            messages.success(request, "Vos préférences de notification ont été enregistrées !")
            return redirect('accounts:settings')

    return render(request, 'accounts/settings.html', {
        'form': form,
        'password_form': password_form
    })


@login_required
def subscription_view(request):
    return render(request, 'accounts/subscription.html')
