from django.contrib import admin

from .models import (
    CV,
    Diplome,
    Experience,
    Competence,
    CategorieCompetence
)


@admin.register(CV)
class CVAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "profil",
        "titre",
        "created_at",
        "updated_at"
    )

    search_fields = (
        "titre",
        "profil__user__username",
        "profil__nom",
        "profil__prenom"
    )


@admin.register(Diplome)
class DiplomeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "titre",
        "etablissement",
        "niveau",
        "annee_debut",
        "annee_obtention",
        "en_cours",
        "cv"
    )

    list_filter = (
        "niveau",
        "en_cours"
    )

    search_fields = (
        "titre",
        "etablissement",
        "specialite"
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "poste",
        "entreprise",
        "type_contrat",
        "poste_actuel",
        "date_debut",
        "date_fin",
        "cv"
    )

    list_filter = (
        "type_contrat",
        "poste_actuel"
    )

    search_fields = (
        "poste",
        "entreprise",
        "ville"
    )


@admin.register(CategorieCompetence)
class CategorieCompetenceAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nom"
    )

    search_fields = (
        "nom",
    )


@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nom",
        "categorie"
    )

    list_filter = (
        "categorie",
    )

    search_fields = (
        "nom",
    )