from django.db import models
from django.contrib.auth.models import User

class ScoreHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores')
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
