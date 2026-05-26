from django import forms
from .models import Diplome, Experience, Competence

class DiplomeForm(forms.ModelForm):

    class Meta:
        model = Diplome
        exclude = ['cv']
        fields = [
            'titre',
            'etablissement',
            'niveau',
            'specialite',
            'annee_debut',
            'annee_obtention',
            'en_cours',
            'description'
        ]

class ExperienceForm(forms.ModelForm):

    class Meta:
        model = Experience
        exclude = ['cv']
        fields = [
            'poste',
            'entreprise',
            'ville',
            'type_contrat',
            'date_debut',
            'date_fin',
            'poste_actuel',
            'description'
        ]

class CompetenceForm(forms.Form):
    
    competences = forms.ModelMultipleChoiceField(
        queryset = Competence.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False
    )