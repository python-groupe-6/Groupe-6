from django import forms

class QuizSetupForm(forms.Form):
    SOURCE_CHOICES = [
        ('document', 'Document (PDF, Word)'),
        ('youtube', 'Lien YouTube'),
        ('image', 'Photo / Image (OCR)')
    ]
    source_type = forms.ChoiceField(
        label="Source du contenu",
        choices=SOURCE_CHOICES,
        initial='document',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    document = forms.FileField(
        label="Document",
        required=False,
        widget=forms.FileInput(attrs={'accept': '.pdf,.docx', 'class': 'form-control'})
    )
    youtube_url = forms.URLField(
        label="URL YouTube",
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.youtube.com/watch?v=...'})
    )
    image = forms.ImageField(
        label="Image / Capture d'écran",
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control'})
    )
    num_questions = forms.IntegerField(

        label="Nombre de questions",
        initial=5,
        min_value=1,
        max_value=20,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    difficulty = forms.ChoiceField(
        label="Difficulté",
        choices=[
            ('Standard', 'Standard'),
            ('Intermédiaire', 'Intermédiaire'),
            ('Avancée', 'Avancée'),
            ('Expert', 'Expert')
        ],
        initial='Standard',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    time_limit = forms.IntegerField(
        label="Durée du quiz (minutes)",
        initial=5,
        min_value=1,
        max_value=60,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    is_exam_mode = forms.BooleanField(
        label="Mode Examen Blanc",
        required=False,
        help_text="Chronomètre strict, pas d'explication immédiate et navigation restreinte.",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
