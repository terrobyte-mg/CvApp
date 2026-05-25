from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Mot de passe',
                'id': 'register_password1'
            }
        )
    )

    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirmer le mot de passe',
                'id': 'register_password2'
            }
        )
    )

    class Meta:
        
        model = User

        fields = ['username', 'email']

        widgets = {

            'username': forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Adresse email'})

        }
    
    def clean(self):
        
        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        
        return cleaned_data
    
    def clean_email(self):

        email = self.cleaned_data.get('email')

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