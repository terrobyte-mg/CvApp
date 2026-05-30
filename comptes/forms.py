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

        # Regex RFC 5322 - exige au moins un TLD (.com, .fr, etc)
        pattern = r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$'

        if not re.match(pattern, email):
            raise ValidationError("Adresse email invalide.")
        
        try:
            username, domain = email.rsplit('@', 1)
        except ValueError:
            raise ValidationError("Adresse email invalide.")

        if len(username) < 2:
            raise ValidationError("Partie avant @ doit contenir au moins 2 caractères.")
        
        if len(username) > 64:
            raise ValidationError("Partie avant @ trop longue (max 64 caractères).")
        
        if len(email) > 254:
            raise ValidationError("Adresse email trop longue (max 254 caractères).")
        
        if domain.startswith('.') or domain.endswith('.'):
            raise ValidationError("Domaine email invalide.")
        
        if '..' in domain:
            raise ValidationError("Domaine email invalide (points consécutifs).")
        
        # Vérifier qu'il y a au moins un point dans le domaine (TLD)
        if '.' not in domain:
            raise ValidationError("Domaine email doit avoir une extension (.com, .fr, etc).")
        
        # Liste complète de domaines temporaires/jetables
        blocked_domains = [
            # Populaires
            "mailinator.com",
            "tempmail.com",
            "guerrillamail.com",
            "10minutemail.com",
            "throwaway.email",
            "temp-mail.org",
            "maildrop.cc",
            "trash-mail.com",
            "sharklasers.com",
            "grr.la",
            # Plus de jetables
            "tempmail.io",
            "yopmail.com",
            "trashmail.com",
            "fakeinbox.com",
            "spam4.me",
            "mailnesia.com",
            "guerrillamail.info",
            "tmail.com",
            "temp-mail.io",
            "maildrop.cc",
            "mytrashmail.com",
            "fake-mail.com",
            "fakemail.net",
        ]

        if domain in blocked_domains:
            raise ValidationError("Domaine email temporaire non autorisé.")

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