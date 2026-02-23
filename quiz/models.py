from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=50)
    time_limit = models.IntegerField(default=5, help_text="Time limit in minutes")
    is_exam_mode = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.difficulty})"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    options = models.JSONField() # Stores the list of options
    correct_answer = models.CharField(max_length=255)
    explanation = models.TextField(blank=True)

    def __str__(self):
        return self.text[:50]

class ScoreHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores')
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.IntegerField()
    total_questions = models.IntegerField(default=5)
    difficulty = models.CharField(max_length=50, default="Standard")
    time_elapsed = models.CharField(max_length=50, help_text="Time taken to complete the quiz")
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']
        verbose_name_plural = "Score Histories"

    def __str__(self):
        return f"{self.user.username} - {self.score}/{self.total_questions} ({self.difficulty})"

class ScoreDetail(models.Model):
    history = models.ForeignKey(ScoreHistory, on_delete=models.CASCADE, related_name='details')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    user_answer = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Detail: {self.question.text[:30]} - {'Correct' if self.is_correct else 'Wrong'}"


class Flashcard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcards')
    question = models.TextField()
    answer = models.TextField()
    explanation = models.TextField(blank=True)
    
    # SRS Fields (SM-2 Algorithm)
    interval = models.IntegerField(default=0) # days
    easiness_factor = models.FloatField(default=2.5)
    repetition_count = models.IntegerField(default=0)
    next_review_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Flashcard: {self.question[:30]}"
    
    def update_srs(self, quality):
        """
        quality: 0-5 (0 = forgot, 5 = perfect)
        Based on SM-2 Algorithm
        """
        if quality >= 3:
            if self.repetition_count == 0:
                self.interval = 1
            elif self.repetition_count == 1:
                self.interval = 6
            else:
                self.interval = round(self.interval * self.easiness_factor)
            self.repetition_count += 1
        else:
            self.repetition_count = 0
            self.interval = 1
        
        # Update easiness factor
        self.easiness_factor = max(1.3, self.easiness_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
        
        from datetime import date, timedelta
        self.next_review_date = date.today() + timedelta(days=self.interval)
        self.save()

