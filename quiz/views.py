import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import QuizSetupForm
from .services import QuizGeneratorService, PDFProcessor
from .models import ScoreHistory

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
            
            # 3. Store in Session
            request.session['quiz_data'] = quiz_data
            request.session['quiz_config'] = {
                'num_questions': num_questions,
                'difficulty': difficulty
            }
            
            return redirect('quiz:quiz_take')

    else:
        form = QuizSetupForm()
    
    return render(request, 'quiz/quiz_setup.html', {'form': form})

@login_required
def quiz_take(request):
    quiz_data = request.session.get('quiz_data')
    if not quiz_data:
        return redirect('quiz:quiz_setup')

    if request.method == 'POST':
        score = 0
        results = []
        
        for i, question in enumerate(quiz_data):
            user_answer = request.POST.get(f'question_{i}')
            correct_answer = question['answer']
            is_correct = user_answer == correct_answer
            if is_correct:
                score += 1
            
            results.append({
                'question': question['question'],
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'explanation': question.get('explanation', '')
            })

        # Save Score
        config = request.session.get('quiz_config', {})
        ScoreHistory.objects.create(
            user=request.user,
            score=score,
            total_questions=len(quiz_data),
            difficulty=config.get('difficulty', 'Standard'),
            time_elapsed="N/A" # To implement timer later
        )
        
        # Clear session
        del request.session['quiz_data']
        
        # Pass full results to template
        return render(request, 'quiz/quiz_result.html', {
            'score': score,
            'total': len(quiz_data),
            'results': results
        })

    return render(request, 'quiz/quiz_take.html', {'quiz_data': quiz_data})

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

