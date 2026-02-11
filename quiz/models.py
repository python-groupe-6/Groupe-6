from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=50)
    time_limit = models.IntegerField(default=5, help_text="Time limit in minutes")
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
