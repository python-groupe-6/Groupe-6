import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import QuizSetupForm
from .services import QuizGeneratorService, PDFProcessor
from .models import ScoreHistory, Quiz, Question

@login_required
def quiz_setup(request):
    if request.method == 'POST':
        form = QuizSetupForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Process PDF
            pdf_file = request.FILES['document']
            text = PDFProcessor.extract_text(pdf_file)
            
            if not text:
                form.add_error('document', "Impossible de lire le fichier PDF.")
                return render(request, 'quiz/quiz_setup.html', {'form': form})

            # 2. Generate Quiz
            service = QuizGeneratorService()
            num_questions = form.cleaned_data['num_questions']
            difficulty = form.cleaned_data['difficulty']
            
            quiz_data = service.generate_quiz(text, num_questions, difficulty)
            
            # 3. Create Quiz in Database
            quiz_obj = Quiz.objects.create(
                user=request.user,
                title=f"Quiz sur {pdf_file.name}",
                difficulty=difficulty,
                time_limit=form.cleaned_data['time_limit']
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
            'results': results
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

