from django import forms

class QuizSetupForm(forms.Form):
    document = forms.FileField(
        label="Document (PDF ou Word)",
        help_text="Téléchargez votre cours au format PDF ou DOCX.",
        widget=forms.FileInput(attrs={'accept': '.pdf,.docx'})
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
