import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import QuizSetupForm
from .services import QuizGeneratorService, DocumentProcessor
from .models import ScoreHistory, Quiz, Question

@login_required
def quiz_setup(request):
    if request.method == 'POST':
        form = QuizSetupForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Process Document (PDF or Word)
            doc_file = request.FILES['document']
            text = DocumentProcessor.extract_text(doc_file)
            
            if not text:
                form.add_error('document', "Impossible de lire le fichier. Formats acceptés : PDF, DOCX.")
                return render(request, 'quiz/quiz_setup.html', {'form': form})

            # 2. Generate Quiz
            service = QuizGeneratorService()
            num_questions = form.cleaned_data['num_questions']
            difficulty = form.cleaned_data['difficulty']
            
            quiz_data = service.generate_quiz(text, num_questions, difficulty)
            
            # 3. Create Quiz in Database
            quiz_obj = Quiz.objects.create(
                user=request.user,
                title=f"Quiz sur {doc_file.name}",
                difficulty=difficulty,
                time_limit=form.cleaned_data['time_limit'],
                is_exam_mode=form.cleaned_data['is_exam_mode']
            )
            
            # 4. Create Questions in Database
            for q in quiz_data:
                Question.objects.create(
                    quiz=quiz_obj,
                    text=q['question'],
                    options=q['options'],
                    correct_answer=q['answer'],
                    explanation=q.get('explanation', '')
                )
            
            # 5. Store Quiz ID in Session
            request.session['quiz_id'] = quiz_obj.id
            
            return redirect('quiz:quiz_take')

    else:
        form = QuizSetupForm()
    
    return render(request, 'quiz/quiz_setup.html', {'form': form})

@login_required
def quiz_take(request):
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
            
            results.append({
                'question': question.text,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'explanation': question.explanation
            })

        # Save Score
        time_elapsed = request.POST.get('time_elapsed', 'N/A')
        ScoreHistory.objects.create(
            user=request.user,
            quiz=quiz_obj,
            score=score,
            total_questions=questions.count(),
            difficulty=quiz_obj.difficulty,
            time_elapsed=time_elapsed
        )
        
        # Clear session
        del request.session['quiz_id']
        
        # Pass full results to template
        return render(request, 'quiz/quiz_result.html', {
            'score': score,
            'total': questions.count(),
            'results': results,
            'quiz_obj': quiz_obj
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
        
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 20, f"Flashcards : {quiz_obj.title}", ln=True, align='C')
        pdf.ln(10)
        
        for i, q in enumerate(questions):
            # Question Card
            pdf.set_fill_color(240, 240, 255)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, f"CARTE {i+1} : QUESTION", ln=True, fill=True)
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 10, q.text, border=1)
            
            # Answer Card
            pdf.set_fill_color(240, 255, 240)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, "RÉPONSE CORRECTE", ln=True, fill=True)
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 10, f"-> {q.correct_answer}", ln=True, border=1)
            
            # Explanation
            if q.explanation:
                pdf.set_fill_color(255, 250, 240)
                pdf.set_font("Arial", 'I', 10)
                pdf.cell(0, 8, "EXPLICATION / ANALYSE", ln=True, fill=True)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 8, q.explanation, border=1)
            
            pdf.ln(15)
            
        filename = f"Flashcards_{quiz_obj.id}.pdf"
        pdf_output = pdf.output(dest='S')
        buffer = io.BytesIO(pdf_output)
        buffer.seek(0)
        
        return FileResponse(buffer, as_attachment=True, filename=filename)
        
    except Quiz.DoesNotExist:
        return HttpResponse(status=404)
    except Exception as e:
        print(f"PDF Error: {e}")
        return HttpResponse(status=500)
