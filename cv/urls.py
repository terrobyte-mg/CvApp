from django.urls import path
from .views import (
    cv_manager,
    profil_edit,
    diplome_list,
    diplome_create,
    diplome_update,
    diplome_delete,
    experience_list,
    experience_create,
    experience_update,
    experience_delete,
    competence_manage,
    cv_builder,
    cv_preview,
)

urlpatterns = [
    path("manager/", cv_manager, name="cv_manager"),
    path("profil/", profil_edit, name="profil_edit"),
    path("diplomes/", diplome_list, name="diplome_list"),
    path("diplomes/add/", diplome_create, name="diplome_create"),
    path("diplomes/<int:pk>/edit/", diplome_update, name="diplome_update"),
    path("diplomes/<int:pk>/delete/", diplome_delete, name="diplome_delete"),
    path("experiences/", experience_list, name="experience_list"),
    path("experiences/add/", experience_create, name="experience_create"),
    path("experiences/<int:pk>/edit/", experience_update, name="experience_update"),
    path("experiences/<int:pk>/delete/", experience_delete, name="experience_delete"),
    path("competences/", competence_manage, name="competence_manage"),
    path("builder/", cv_builder, name="cv_builder"),
    path("preview/", cv_preview, name="cv_preview")
]