from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from comptes.models import Profil

class CV(models.Model):
    profil = models.OneToOneField(
        Profil, 
        on_delete=models.CASCADE,
        related_name='cv'
    )
    
    titre = models.CharField(
        max_length=200, 
        verbose_name="Titre du CV",
        help_text="Ex: Développeur Fullstack / Technicien Supérieur en Génie Logiciel"
    )
    
    introduction = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Accroche / Objectif professionnel"
    )

    # Renommé en 'competences' (au pluriel) pour respecter les conventions
    competences = models.ManyToManyField(
        'Competence',
        blank=True,
        related_name='cvs'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")

    class Meta:
        verbose_name = "CV"
        verbose_name_plural = "CV"  # Évite le "CVs" automatique dans l'admin Django

    def __str__(self):
        return f"CV - {self.profil.user.username} ({self.titre})"
    
class CVSettings(models.Model):

    cv = models.OneToOneField(
        "CV",
        on_delete=models.CASCADE,
        related_name="settings"
    )

    TEMPLATE_CHOICES = [
        ("minimal", "Minimaliste"),
        ("modern", "Moderne"),
        ("future", "Futuriste"),
    ]

    template = models.CharField(
        max_length=20,
        choices=TEMPLATE_CHOICES,
        default="minimal"
    )

    font_family = models.CharField(
        max_length=100,
        default="Arial"
    )

    show_profile = models.BooleanField(default=True)
    show_diplomes = models.BooleanField(default=True)
    show_experiences = models.BooleanField(default=True)
    show_competences = models.BooleanField(default=True)

    def __str__(self):
        return f"Settings CV {self.cv.id}"
    

class Diplome(models.Model):
    NIVEAU_CHOICES = [
        ('BAC', 'Baccalauréat'),
        ('BAC+2', 'DTS, BTS, DUT'),
        ('BAC+3', 'DTSS, Licence, Licence Pro, BUT'),
        ('BAC+5', "Master, Diplôme d'Ingénieur"),
        ('BAC+8', 'Doctorat'),
        ('Autre', 'Autre niveau de diplôme')
    ]

    cv = models.ForeignKey(
        CV,
        on_delete=models.CASCADE,
        related_name='diplomes'
    )

    titre = models.CharField(max_length=200, verbose_name="Titre du diplôme")
    etablissement = models.CharField(max_length=200, verbose_name="Établissement d'obtention")
    niveau = models.CharField(max_length=10, choices=NIVEAU_CHOICES, verbose_name="Niveau du diplôme")
    specialite = models.CharField(max_length=200, blank=True, verbose_name="Spécialité / Option")
    annee_debut = models.PositiveIntegerField(verbose_name="Année de début d'études")
    annee_obtention = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Année d'obtention du diplôme (ou prévue)"
    )
    en_cours = models.BooleanField(default=False, verbose_name="En cours d'obtention")
    description = models.TextField(blank=True, verbose_name="Description ou projets marquants liés à ce diplôme")

    class Meta:
        ordering = ['-annee_obtention', '-annee_debut']
        verbose_name = "Diplôme"
        verbose_name_plural = "Diplômes"

    def clean(self):
        super().clean()

        if self.en_cours and self.annee_obtention:
            raise ValidationError({
                "annee_obtention": "Un diplôme en cours ne peut pas avoir d'année d'obtention renseignée."
            })

        year = timezone.now().year

        if self.annee_debut and self.annee_debut > year:
            raise ValidationError({
                "annee_debut": "L'année de début ne peut pas être dans le futur."
            })

        if self.annee_obtention:
            if self.annee_obtention > year + 8:
                raise ValidationError({
                    "annee_obtention": "L'année d'obtention ne peut pas être trop éloignée dans le futur."
                })

            if self.annee_debut and self.annee_obtention < self.annee_debut:
                raise ValidationError({
                    "annee_obtention": "L'année d'obtention ne peut pas être antérieure à l'année de début."
                })
            
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.titre} - {self.etablissement} ({self.annee_obtention or 'En cours'})"    


class Experience(models.Model):
    CONTRAT_CHOICES = [
        ('CDI', 'CDI'),
        ('CDD', 'CDD'),
        ('STAGE', 'Stage'),
        ('ALTER', 'Alternance'),
        ('FREELANCE', 'Freelance / Indépendant'),
        ('INTERIM', 'Intérim'),
    ]

    cv = models.ForeignKey(
        CV,
        on_delete=models.CASCADE,
        related_name='experiences'
    )

    poste = models.CharField(max_length=200, verbose_name="Intitulé du poste", blank=True)
    entreprise = models.CharField(max_length=200, verbose_name="Entreprise / Organisation", blank=True)
    ville = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ville")
    type_contrat = models.CharField(
        max_length=15, 
        choices=CONTRAT_CHOICES,
        verbose_name="Type de contrat",
        blank=True
    )
    date_debut = models.DateField(verbose_name="Date de début", blank=True)
    date_fin = models.DateField(blank=True, null=True, verbose_name="Date de fin")
    poste_actuel = models.BooleanField(default=False, verbose_name="J'occupe actuellement ce poste", blank=True)
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Missions et réalisations",
        help_text="Détaillez vos tâches principales et vos résultats."
    )

    class Meta:
        ordering = ['-poste_actuel', '-date_debut']
        verbose_name = "Expérience Professionnelle"
        verbose_name_plural = "Expériences Professionnelles"

    def clean(self):
        super().clean()

        if self.poste_actuel and self.date_fin:
            raise ValidationError({
                "date_fin": "Un poste actuel ne peut pas avoir de date de fin renseignée."
            })
        
        if self.poste or self.entreprise or self.ville and not self.date_fin and not self.poste_actuel:
            raise ValidationError({
                "date_fin": "Veuillez indiquer une date de fin ou cocher poste actuel."
            })
        
        if self.date_debut and self.date_fin and self.date_fin < self.date_debut:
            raise ValidationError({
                "date_fin": "La date de fin ne peut pas être antérieure à la date de début."
            })
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        status = "Présent" if self.poste_actuel else (self.date_fin or "Non renseignée")
        return f"{self.poste} chez {self.entreprise} ({self.date_debut} - {status})"
    

class CategorieCompetence(models.Model):
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la catégorie")

    class Meta:
        verbose_name = "Catégorie de compétence"
        verbose_name_plural = "Catégories de compétences"

    def __str__(self):
        return self.nom


class Competence(models.Model):
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la compétence")
    categorie = models.ForeignKey(
        CategorieCompetence, 
        on_delete=models.CASCADE, 
        related_name="competences",
        verbose_name="Catégorie"
    )

    class Meta:
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} ({self.categorie.nom})"