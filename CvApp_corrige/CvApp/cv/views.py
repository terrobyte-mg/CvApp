from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CV, CVSettings, Diplome, Experience
from comptes.forms import ProfilForm
from .forms import CVForm, CompetenceForm, DiplomeForm, ExperienceForm


@login_required
def cv_manager(request):
    profil = request.user.profil
    cv, created = CV.objects.get_or_create(profil=profil)
    context = {
        "profil": profil,
        "cv": cv
    }
    return render(request, "cv/manager.html", context)


@login_required
def profil_edit(request):
    profil = request.user.profil
    if request.method == "POST":
        form = ProfilForm(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect("cv_manager")
    else:
        form = ProfilForm(instance=profil)
    return render(request, "cv/profil_edit.html", {"form": form})


@login_required
def cv_info_edit(request):
    """Vue pour modifier le titre et l'introduction du CV"""
    cv = CV.objects.get(profil=request.user.profil)
    if request.method == "POST":
        form = CVForm(request.POST, instance=cv)
        if form.is_valid():
            form.save()
            messages.success(request, "Informations du CV mises à jour.")
            return redirect("cv_manager")
    else:
        form = CVForm(instance=cv)
    return render(request, "cv/cv_info_edit.html", {"form": form, "cv": cv})


@login_required
def diplome_list(request):
    cv = CV.objects.get(profil=request.user.profil)
    return render(request, "cv/diplome_list.html", {
        "cv": cv,
        "diplomes": cv.diplomes.all()
    })


@login_required
def diplome_create(request):
    cv = CV.objects.get(profil=request.user.profil)
    if request.method == "POST":
        form = DiplomeForm(request.POST)
        if form.is_valid():
            diplome = form.save(commit=False)
            diplome.cv = cv
            diplome.save()
            messages.success(request, "Diplôme ajouté avec succès.")
            return redirect("diplome_list")
    else:
        form = DiplomeForm()
    return render(request, "cv/diplome_form.html", {"form": form})


@login_required
def diplome_update(request, pk):
    diplome = get_object_or_404(Diplome, pk=pk, cv__profil=request.user.profil)
    if request.method == "POST":
        form = DiplomeForm(request.POST, instance=diplome)
        if form.is_valid():
            form.save()
            messages.success(request, "Diplôme modifié avec succès.")
            return redirect("diplome_list")
    else:
        form = DiplomeForm(instance=diplome)
    return render(request, "cv/diplome_form.html", {"form": form})


@login_required
def diplome_delete(request, pk):
    diplome = get_object_or_404(Diplome, pk=pk, cv__profil=request.user.profil)
    if request.method == "POST":
        diplome.delete()
        messages.success(request, "Diplôme supprimé.")
        return redirect("diplome_list")
    return render(request, "cv/diplome_confirm_delete.html", {"diplome": diplome})


@login_required
def experience_list(request):
    cv = CV.objects.get(profil=request.user.profil)
    return render(request, "cv/experience_list.html", {
        "cv": cv,
        "experiences": cv.experiences.all()
    })


@login_required
def experience_create(request):
    cv = CV.objects.get(profil=request.user.profil)
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.cv = cv
            exp.save()
            messages.success(request, "Expérience ajoutée avec succès.")
            return redirect("experience_list")
    else:
        form = ExperienceForm()
    return render(request, "cv/experience_form.html", {"form": form})


@login_required
def experience_update(request, pk):
    exp = get_object_or_404(Experience, pk=pk, cv__profil=request.user.profil)
    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=exp)
        if form.is_valid():
            form.save()
            messages.success(request, "Expérience modifiée avec succès.")
            return redirect("experience_list")
    else:
        form = ExperienceForm(instance=exp)
    return render(request, "cv/experience_form.html", {"form": form})


@login_required
def experience_delete(request, pk):
    exp = get_object_or_404(Experience, pk=pk, cv__profil=request.user.profil)
    if request.method == "POST":
        exp.delete()
        messages.success(request, "Expérience supprimée.")
        return redirect("experience_list")
    return render(request, "cv/experience_confirm_delete.html", {"experience": exp})


@login_required
def competence_manage(request):
    cv = CV.objects.get(profil=request.user.profil)
    if request.method == "POST":
        form = CompetenceForm(request.POST)
        if form.is_valid():
            cv.competences.set(form.cleaned_data["competences"])
            messages.success(request, "Compétences mises à jour.")
            return redirect("competence_manage")
    else:
        form = CompetenceForm(initial={"competences": cv.competences.all()})
    return render(request, "cv/competence_form.html", {"form": form, "cv": cv})


@login_required
def cv_builder(request):
    cv = CV.objects.get(profil=request.user.profil)
    settings, created = CVSettings.objects.get_or_create(cv=cv)

    if request.method == "POST":
        settings.template = request.POST.get("template", "minimal")
        settings.font_family = request.POST.get("font_family", "Arial")
        settings.show_profile = "show_profile" in request.POST
        settings.show_diplomes = "show_diplomes" in request.POST
        settings.show_experiences = "show_experiences" in request.POST
        settings.show_competences = "show_competences" in request.POST
        settings.save()
        messages.success(request, "Paramètres du CV sauvegardés.")

    return render(request, "cv/cv_builder.html", {
        "cv": cv,
        "settings": settings,
        "profil": request.user.profil,
        "diplomes": cv.diplomes.all(),
        "experiences": cv.experiences.all(),
        "competences": cv.competences.all(),
    })


@login_required
def cv_view(request):
    cv = CV.objects.get(profil=request.user.profil)
    settings, _ = CVSettings.objects.get_or_create(cv=cv)

    template_map = {
        "minimal": "cv/minimal.html",
        "modern": "cv/modern.html",
        "future": "cv/future.html",
    }

    return render(request, template_map.get(settings.template, "cv/minimal.html"), {
        "cv": cv,
        "settings": settings,
        "profil": request.user.profil,
        "diplomes": cv.diplomes.all(),
        "experiences": cv.experiences.all(),
        "competences": cv.competences.all(),
    })


@xframe_options_exempt
@login_required
def cv_preview(request):
    cv = CV.objects.get(profil=request.user.profil)
    template = request.GET.get("template", "minimal")

    template_map = {
        "minimal": "cv/minimal.html",
        "modern": "cv/modern.html",
        "future": "cv/future.html",
    }

    return render(request, template_map.get(template, "cv/minimal.html"), {
        "cv": cv,
        "profil": request.user.profil,
        "diplomes": cv.diplomes.all(),
        "experiences": cv.experiences.all(),
        "competences": cv.competences.all(),
        "template": template,
    })
