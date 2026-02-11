from django import forms
from .models import Testimonial, ContactMessage

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Partagez votre expérience avec EduQuiz AI...'
            }),
            'rating': forms.Select(
                choices=[(i, f'{i} étoile{"s" if i > 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'form-select'}
            )
        }
        labels = {
            'content': 'Votre avis',
            'rating': 'Votre note'
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'Votre nom complet'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'votre@email.com'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-select rounded-3'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control rounded-3',
                'rows': 4,
                'placeholder': 'Comment pouvons-nous vous aider ?'
            }),
        }
