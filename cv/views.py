from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import CV, Diplome, Experience
from comptes.forms import ProfilForm
from .forms import CompetenceForm, DiplomeForm, ExperienceForm


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
            return redirect("cv_manager")

    else:
        form = ProfilForm(instance=profil)

    return render(request, "cv/profil_edit.html", {
        "form": form
    })

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
            return redirect("diplome_list")

    else:
        form = DiplomeForm()

    return render(request, "cv/diplome_form.html", {
        "form": form
    })

@login_required
def diplome_update(request, pk):

    diplome = get_object_or_404(
        Diplome,
        pk=pk,
        cv__profil=request.user.profil
    )

    if request.method == "POST":
        form = DiplomeForm(request.POST, instance=diplome)

        if form.is_valid():
            form.save()
            return redirect("diplome_list")

    else:
        form = DiplomeForm(instance=diplome)

    return render(request, "cv/diplome_form.html", {
        "form": form
    })

@login_required
def diplome_delete(request, pk):

    diplome = get_object_or_404(
        Diplome,
        pk=pk,
        cv__profil=request.user.profil
    )

    if request.method == "POST":
        diplome.delete()
        return redirect("diplome_list")

    return render(request, "cv/diplome_confirm_delete.html", {
        "diplome": diplome
    })

@login_required
def experience_list(request):

    cv = CV.objects.get(profil=request.user.profil)

    return render(request, "cv/experience_list.html", {
        "cv": cv,
        "experiences": cv.experiences.all()
    })


from django.shortcuts import render, redirect, get_object_or_404
from cv.forms import ExperienceForm
from cv.models import CV

@login_required
def experience_create(request):

    cv = CV.objects.get(profil=request.user.profil)

    if request.method == "POST":
        form = ExperienceForm(request.POST)

        if form.is_valid():
            exp = form.save(commit=False)
            exp.cv = cv
            exp.save()
            return redirect("experience_list")

    else:
        form = ExperienceForm()

    return render(request, "cv/experience_form.html", {
        "form": form
    })

@login_required
def experience_update(request, pk):

    exp = get_object_or_404(
        Experience,
        pk=pk,
        cv__profil=request.user.profil
    )

    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=exp)

        if form.is_valid():
            form.save()
            return redirect("experience_list")

    else:
        form = DiplomeForm(instance=exp)

    return render(request, "cv/experience_form.html", {
        "form": form
    })

@login_required
def experience_delete(request, pk):

    exp = get_object_or_404(
        Experience,
        pk=pk,
        cv__profil=request.user.profil
    )

    if request.method == "POST":
        exp.delete()
        return redirect("experience_list")

    return render(request, "cv/experience_confirm_delete.html", {
        "experience": exp
    })

@login_required
def competence_manage(request):

    cv = CV.objects.get(profil=request.user.profil)

    if request.method == "POST":

        form = CompetenceForm(request.POST)

        if form.is_valid():

            cv.competences.set(form.cleaned_data["competences"])
            return redirect("competence_manage")

    else:

        form = CompetenceForm(initial={
            "competences": cv.competences.all()
        })

    return render(request, "cv/competence_form.html", {
        "form": form,
        "cv": cv
    })