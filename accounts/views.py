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

# SPA Password Reset Views
import json
import random
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def password_reset_spa(request):
    return render(request, 'registration/password_reset_spa.html')

@require_POST
def send_reset_code(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({'success': False, 'message': 'Email manquant'}, status=400)
            
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Pour la sécurité, on ne dit pas si l'email n'existe pas, mais on fait semblant
            # Cela évite le "User Enumeration"
            # Cependant, pour ce design spécifique, si on veut une UX fluide...
            # On va simuler un succès mais ne rien envoyer.
            # OU on renvoie une erreur si c'est ce que veut le client (moins sécure)
            # Le client veut que ça marche. On va renvoyer success.
            return JsonResponse({'success': True})

        # Générer le code
        code = str(random.randint(100000, 999999))
        
        # Stocker en session
        request.session['reset_code'] = code
        request.session['reset_email'] = email
        request.session['reset_verified'] = False
        request.session.save() # Forcer la sauvegarde
        
        # Envoyer l'email
        send_mail(
            'Votre code de réinitialisation EduQuiz AI',
            f'Votre code de vérification est : {code}',
            'noreply@eduquiz.ai',
            [email],
            fail_silently=False,
        )
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@require_POST
def verify_reset_code(request):
    try:
        data = json.loads(request.body)
        code = data.get('code')
        
        session_code = request.session.get('reset_code')
        
        if not session_code:
             return JsonResponse({'success': False, 'message': 'Session expirée'}, status=400)
             
        if code == session_code:
            request.session['reset_verified'] = True
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Code incorrect'}, status=400)
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@require_POST
def reset_password_action(request):
    try:
        data = json.loads(request.body)
        new_password = data.get('password')
        
        if not request.session.get('reset_verified'):
            return JsonResponse({'success': False, 'message': 'Vérification requise'}, status=403)
            
        email = request.session.get('reset_email')
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            
            # Update session auth hash? No, user needs to login again usually.
            # But let's clean the session
            del request.session['reset_code']
            del request.session['reset_email']
            del request.session['reset_verified']
            
            return JsonResponse({'success': True})
            
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Utilisateur introuvable'}, status=404)
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
