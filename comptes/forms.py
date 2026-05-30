import re

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from comptes.models import Profil


class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Mot de passe',
                'id': 'register_password1'
            }
        ),
        min_length=8,
    )

    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirmer le mot de passe',
                'id': 'register_password2'
            }
        ),
        min_length=8,
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Adresse email',
            }
        )
    )

    class Meta:
        
        model = User

        fields = ['username', 'email']

        widgets = {

            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Nom d\'utilisateur',
                    'id': 'id_username'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Adresse email',
                    'id': 'id_email'
                }
            )

        }
    
    def clean(self):
        
        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        
        return cleaned_data
    
    def clean_email(self):

        email = self.cleaned_data.get('email')

        if not email:
            raise ValidationError("Email requis.")
        
        email = email.lower().strip()

        pattern = r'^[a-zA-Z0-9._%+-]{1,}@[a-zA-Z0-9.-]{3,}\.[a-zA-Z]{2,}$'

        if not re.match(pattern, email):
            raise ValidationError("Adresse email invalide.")
        
        username, domain = email.split('@')

        if len(username) < 1:
            raise ValidationError("Partie avant @ trop courte.")
        
        if len(domain.split('.')[0]) < 2:
            raise ValidationError("Domaine email invalide.")
        
        blocked_domains = [
            "mailinator.com",
            "tempmail.com",
            "guerrillamail.com"
        ]

        if domain in blocked_domains:
            raise ValidationError("Emails temporaires nnon autorisés.")

        if User.objects.filter(email=email).exists():
            raise ValidationError("Cette adresse email est déjà utilisée.")
        
        return email
    
    def save(self, commit=True):

        user = super().save(commit = False)

        user.set_password(self.cleaned_data.get('password1'))

        if commit:
            user.save()

        return user
    
class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'})
    )

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Mot de passe',
                'id': 'login_password'
            }
        )
    )

class ProfilForm(forms.ModelForm):

    class Meta:
        model = Profil
        fields = ['nom', 'prenom', 'adresse', 'bio', 'photo', 'telephone']