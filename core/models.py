from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials')
    content = models.TextField(max_length=500, help_text="Partagez votre expérience avec EduQuiz AI")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Note de 1 à 5 étoiles"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)  # Auto-approve for now
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
    
    def __str__(self):
        return f"{self.user.username} - {self.rating}★"

class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('AVIS', 'Donner un avis'),
        ('SUGGESTION', 'Faire une suggestion'),
        ('SUPPORT', 'Support technique'),
        ('AUTRE', 'Autre'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Adresse email")
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='AVIS', verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"

    def __str__(self):
        return f"{self.name} - {self.get_subject_display()}"
