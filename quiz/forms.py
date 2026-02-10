from django import forms

class QuizSetupForm(forms.Form):
    document = forms.FileField(
        label="Document (PDF)",
        help_text="Téléchargez votre cours au format PDF.",
        widget=forms.FileInput(attrs={'accept': '.pdf'})
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
