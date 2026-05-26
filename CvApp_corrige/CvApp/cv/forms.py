from django import forms
from .models import CV, Diplome, Experience, Competence


class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['titre', 'introduction']
        widgets = {
            'titre': forms.TextInput(attrs={
                'placeholder': 'Ex: Développeur Fullstack / Ingénieur Logiciel',
                'class': 'form-input'
            }),
            'introduction': forms.Textarea(attrs={
                'placeholder': 'Décrivez votre objectif professionnel en quelques lignes...',
                'rows': 4,
                'class': 'form-input'
            }),
        }


class DiplomeForm(forms.ModelForm):
    class Meta:
        model = Diplome
        exclude = ['cv']
        fields = [
            'titre', 'etablissement', 'niveau', 'specialite',
            'annee_debut', 'annee_obtention', 'en_cours', 'description'
        ]


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ['cv']
        fields = [
            'poste', 'entreprise', 'ville', 'type_contrat',
            'date_debut', 'date_fin', 'poste_actuel', 'description'
        ]
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }


class CompetenceForm(forms.Form):
    competences = forms.ModelMultipleChoiceField(
        queryset=Competence.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
