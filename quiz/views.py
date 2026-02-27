import json
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse, FileResponse
from django.contrib import messages
from .forms import QuizSetupForm
from .services import QuizGeneratorService, DocumentProcessor
from .models import ScoreHistory, Quiz, Question, Flashcard, ScoreDetail


@login_required
def quiz_setup(request):
    if request.method == 'POST':
        form = QuizSetupForm(request.POST, request.FILES)
        if form.is_valid():
            source_type = form.cleaned_data['source_type']
            text = ""
            quiz_title = "Quiz sans titre"
            
            from .services import YouTubeProcessor, OCRProcessor
            
            if source_type == 'document':
                doc_file = request.FILES.get('document')
                if not doc_file:
                    form.add_error('document', "Veuillez télécharger un fichier.")
                    return render(request, 'quiz/quiz_setup.html', {'form': form})
                text = DocumentProcessor.extract_text(doc_file)
                quiz_title = f"Quiz sur {doc_file.name}"
                
            elif source_type == 'youtube':
                url = form.cleaned_data.get('youtube_url')
                if not url:
                    form.add_error('youtube_url', "Veuillez saisir une URL YouTube.")
                    return render(request, 'quiz/quiz_setup.html', {'form': form})
                text = YouTubeProcessor.extract_transcript(url)
                quiz_title = "Quiz Vidéo YouTube"
                
            elif source_type == 'image':
                img_file = request.FILES.get('image')
                if not img_file:
                    form.add_error('image', "Veuillez charger une image.")
                    return render(request, 'quiz/quiz_setup.html', {'form': form})
                text = OCRProcessor.extract_text_from_image(img_file)
                quiz_title = f"Quiz Image - {img_file.name}"

            if not text or len(text.strip()) < 50:
                error_msg = "Impossible d'extraire assez de texte de cette source. Vérifiez la source ou réessayez."
                form.add_error(None, error_msg)
                return render(request, 'quiz/quiz_setup.html', {'form': form})

            # 2. Generate Quiz
            service = QuizGeneratorService()
            num_questions = form.cleaned_data['num_questions']
            difficulty = form.cleaned_data['difficulty']
            quiz_data = service.generate_quiz(text, num_questions, difficulty)
            
            # 3. Create Quiz & Questions
            quiz_obj = Quiz.objects.create(
                user=request.user,
                title=quiz_title,
                difficulty=difficulty,
                time_limit=form.cleaned_data['time_limit'],
                is_exam_mode=form.cleaned_data['is_exam_mode']
            )
            for q in quiz_data:
                Question.objects.create(
                    quiz=quiz_obj,
                    text=q['question'],
                    options=q['options'],
                    correct_answer=q['answer'],
                    explanation=q.get('explanation', '')
                )
            request.session['quiz_id'] = quiz_obj.id
            return redirect('quiz:quiz_take')
    else:
        form = QuizSetupForm()
    return render(request, 'quiz/quiz_setup.html', {'form': form})


@login_required
def quiz_take(request, quiz_id=None):
    if quiz_id:
        request.session['quiz_id'] = quiz_id
        
    quiz_id = request.session.get('quiz_id')
    if not quiz_id:
        return redirect('quiz:quiz_setup')

    try:
        quiz_obj = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return redirect('quiz:quiz_setup')

    questions = quiz_obj.questions.all()

    if request.method == 'POST':
        score = 0
        results = []
        
        for i, question in enumerate(questions):
            user_answer = request.POST.get(f'question_{i}')
            correct_answer = question.correct_answer
            is_correct = user_answer == correct_answer
            if is_correct:
                score += 1
            
            # Temporary results for template
            res_item = {
                'question': question,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
            }
            results.append(res_item)

        # Save Score History
        time_elapsed = request.POST.get('time_elapsed', 'N/A')
        score_obj = ScoreHistory.objects.create(
            user=request.user,
            quiz=quiz_obj,
            score=score,
            total_questions=questions.count(),
            difficulty=quiz_obj.difficulty,
            time_elapsed=time_elapsed
        )
        
        # Save detailed score per question
        for res in results:
            ScoreDetail.objects.create(
                history=score_obj,
                question=res['question'],
                is_correct=res['is_correct'],
                user_answer=res['user_answer'] or "Pas de réponse"
            )
        
        # Gamification: Update XP and Streak
        difficulty_map = {"Basique": 1, "Standard": 1.5, "Avancé": 2, "Expert": 2.5}
        multiplier = difficulty_map.get(quiz_obj.difficulty, 1)
        xp_earned = request.user.profile.update_xp_and_streak(score, questions.count(), multiplier)
        
        # Clear session
        del request.session['quiz_id']
        
        # Pass full results to template
        return render(request, 'quiz/quiz_result.html', {
            'score': score,
            'total': questions.count(),
            'quiz_obj': quiz_obj,
            'history_id': score_obj.id,
            'xp_earned': xp_earned,
            'new_streak': request.user.profile.streak

        })

    return render(request, 'quiz/quiz_take.html', {
        'quiz_data': questions,
        'quiz_obj': quiz_obj
    })

@login_required
def quiz_history(request):
    history = ScoreHistory.objects.filter(user=request.user).order_by('-completed_at')
    
    # Calculate stats
    total_quizzes = history.count()
    best_score = 0
    avg_score = 0
    
    if total_quizzes > 0:
        best_score = history.order_by('-score').first().score
        total_points = sum(item.score for item in history)
        avg_score = round(total_points / total_quizzes, 1)

    return render(request, 'quiz/quiz_history.html', {
        'history': history,
        'total_quizzes': total_quizzes,
        'best_score': best_score,
        'avg_score': avg_score
    })

@login_required
def quiz_analysis(request, history_id):
    from django.shortcuts import get_object_or_404
    history_item = get_object_or_404(ScoreHistory, id=history_id, user=request.user)
    questions = []
    if history_item.quiz:
        questions = history_item.quiz.questions.all()
    return render(request, 'quiz/quiz_analysis.html', {
        'history_item': history_item,
        'questions': questions,
        'score_pct': round((history_item.score / history_item.total_questions) * 100) if history_item.total_questions else 0,
    })

from django.http import HttpResponse
from gtts import gTTS
import io

@login_required
def generate_audio(request):
    text = request.GET.get('text', '')
    if not text:
        return HttpResponse(status=400)
    
    try:
        tts = gTTS(text=text, lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return HttpResponse(fp.read(), content_type='audio/mpeg')
    except Exception as e:
        print(f"TTS Error: {e}")
        return HttpResponse(status=500)

from fpdf import FPDF
from django.http import FileResponse

@login_required
def export_flashcards(request, quiz_id):
    try:
        quiz_obj = Quiz.objects.get(id=quiz_id, user=request.user)
        questions = quiz_obj.questions.all()
        
        # Robust text cleaning for PDF (Standard fonts only support Latin-1)
        def clean_text(text):
            if not text: return ""
            return text.encode('latin-1', 'replace').decode('latin-1')

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Title
        pdf.set_font("helvetica", 'B', 20)
        pdf.cell(0, 20, clean_text(f"Flashcards : {quiz_obj.title}"), ln=True, align='C')
        pdf.ln(10)
        
        for i, q in enumerate(questions):
            # Question Card
            pdf.set_fill_color(240, 240, 255)
            pdf.set_font("helvetica", 'B', 12)
            pdf.cell(0, 10, clean_text(f"CARTE {i+1} : QUESTION"), ln=True, fill=True)
            pdf.set_font("helvetica", '', 11)
            pdf.multi_cell(0, 10, clean_text(q.text), border=1)
            
            # Answer Card
            pdf.set_fill_color(240, 255, 240)
            pdf.set_font("helvetica", 'B', 12)
            pdf.cell(0, 10, clean_text("RÉPONSE CORRECTE"), ln=True, fill=True)
            pdf.set_font("helvetica", 'B', 11)
            pdf.cell(0, 10, clean_text(f"-> {q.correct_answer}"), ln=True, border=1)
            
            # Explanation
            if q.explanation:
                pdf.set_fill_color(255, 250, 240)
                pdf.set_font("helvetica", 'I', 10)
                pdf.cell(0, 8, clean_text("EXPLICATION / ANALYSE"), ln=True, fill=True)
                pdf.set_font("helvetica", '', 10)
                pdf.multi_cell(0, 8, clean_text(q.explanation), border=1)
            
            pdf.ln(15)
            
        filename = f"Flashcards_{quiz_obj.id}.pdf"
        pdf_bytes = pdf.output()
        buffer = io.BytesIO(pdf_bytes)
        buffer.seek(0)
        
        return FileResponse(buffer, as_attachment=True, filename=filename)
        
    except Quiz.DoesNotExist:
        return HttpResponse("Quiz non trouvé", status=404)
    except Exception as e:
        with open("debug_quiz.log", "a", encoding="utf-8") as f:
            f.write(f"PDF Export Error for Quiz {quiz_id}: {str(e)}\n")
        return HttpResponse(f"Erreur lors de la génération du PDF : {str(e)}", status=500)

@login_required
@require_POST
def save_flashcard(request):
    try:
        data = json.loads(request.body)
        question_text = data.get('question')
        answer_text = data.get('answer')
        explanation = data.get('explanation', '')
        
        from .models import Flashcard
        Flashcard.objects.create(
            user=request.user,
            question=question_text,
            answer=answer_text,
            explanation=explanation
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
def srs_dashboard(request):
    from datetime import date
    from .models import Flashcard
    flashcards = Flashcard.objects.filter(user=request.user)
    due_today = flashcards.filter(next_review_date__lte=date.today()).count()
    return render(request, 'quiz/srs_dashboard.html', {
        'total_cards': flashcards.count(),
        'due_today': due_today,
        'flashcards': flashcards[:10]
    })

@login_required
def srs_review(request):
    from datetime import date
    from .models import Flashcard
    due_cards = Flashcard.objects.filter(user=request.user, next_review_date__lte=date.today())
    if not due_cards.exists():
        messages.info(request, "Toutes vos flashcards sont à jour ! Revenez plus tard.")
        return redirect('quiz:srs_dashboard')
    
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        quality = int(request.POST.get('quality', 3))
        card = Flashcard.objects.get(id=card_id, user=request.user)
        card.update_srs(quality)
        return redirect('quiz:srs_review')
        
    return render(request, 'quiz/srs_review.html', {'card': due_cards.first(), 'remaining': due_cards.count()})

@login_required
def analytics_dashboard(request):
    from django.db.models import Count
    from django.db.models.functions import TruncDate
    from .models import ScoreHistory, ScoreDetail
    
    # 1. Activity Heatmap Data (last 30 days)
    activity_data = ScoreHistory.objects.filter(user=request.user) \
        .annotate(date=TruncDate('completed_at')) \
        .values('date') \
        .annotate(count=Count('id')) \
        .order_by('date')
    
    activity_json = {str(item['date']): item['count'] for item in activity_data}
    
    # 2. Gap Analysis (AI Feedback)
    details = ScoreDetail.objects.filter(history__user=request.user).order_by('-history__completed_at')[:50]
    service = QuizGeneratorService()
    gap_feedback = service.analyze_gaps(details)
    
    # 3. Overall performance stats
    total_quizzes = ScoreHistory.objects.filter(user=request.user).count()
    avg_score = ScoreHistory.objects.filter(user=request.user).aggregate(models.Avg('score'))['score__avg'] or 0
    
    return render(request, 'quiz/analytics_dashboard.html', {
        'activity_json': json.dumps(activity_json),
        'gap_feedback': gap_feedback,
        'total_quizzes': total_quizzes,
        'avg_score': round(avg_score, 1)
    })

@login_required
@require_POST
def ai_tutor_chat(request):
    import google.generativeai as genai
    import os
    try:
        data = json.loads(request.body)
        question = data.get('question')
        user_msg = data.get('message')
        context = data.get('context', '')
        
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Tu es un tuteur pédagogique expert. 
        Question d'origine : {question}
        Contexte/Explication actuelle : {context}
        L'étudiant demande : {user_msg}
        
        Réponds de manière concise, encourageante et pédagogique pour aider l'étudiant à comprendre en profondeur.
        Utilise du Markdown pour la clarté si nécessaire.
        """
        
        response = model.generate_content(prompt)
        return JsonResponse({'success': True, 'response': response.text})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
def public_library(request):
    from .models import Quiz
    quizzes = Quiz.objects.filter(is_public=True).order_by('-likes', '-created_at')
    return render(request, 'quiz/public_library.html', {'quizzes': quizzes})

@login_required
@require_POST
def toggle_public(request, quiz_id):
    from .models import Quiz
    quiz = get_object_or_404(Quiz, id=quiz_id, user=request.user)
    quiz.is_public = not quiz.is_public
    quiz.save()
    return JsonResponse({'success': True, 'is_public': quiz.is_public})

@login_required
@require_POST
def like_quiz(request, quiz_id):
    from .models import Quiz
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.likes += 1
    quiz.save()
    return JsonResponse({'success': True, 'likes': quiz.likes})



