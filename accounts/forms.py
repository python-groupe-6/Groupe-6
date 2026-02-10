from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Prénom")
    last_name = forms.CharField(max_length=30, required=True, label="Nom")
    email = forms.EmailField(max_length=254, required=True, label="Email")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['email'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['password1'].label = "Mot de passe"
        self.fields['password2'].label = "Confirmer le mot de passe"

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Prénom", required=True)
    last_name = forms.CharField(label="Nom", required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class SettingsUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dark_mode', 'language']
        labels = {
            'dark_mode': 'Mode Sombre',
            'language': 'Langue'
        }
