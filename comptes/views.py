from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.conf import settings

from django.core.files.storage import FileSystemStorage

from comptes.models import Profil
from cv.models import CV

from .forms import RegisterForm, LoginForm, ProfilForm
from cv.forms import DiplomeForm, ExperienceForm, CompetenceForm

from formtools.wizard.views import SessionWizardView


def auth_view(request):

    mode = request.GET.get('mode', 'login')

    login_form = LoginForm(request)
    register_form = RegisterForm()

    # ===== REGISTER =====
    if request.method == 'POST' and 'register_submit' in request.POST:

        mode = 'register'

        register_form = RegisterForm(request.POST)

        if register_form.is_valid():

            register_form.save()

            messages.success(
                request,
                "Compte créé avec succès. Connecte-toi maintenant."
            )

            return redirect('/auth/?mode=login')

    # ===== LOGIN =====
    elif request.method == 'POST' and 'login_submit' in request.POST:

        mode = 'login'

        login_form = LoginForm(request, data=request.POST)

        if login_form.is_valid():

            user = login_form.get_user()

            auth_login(request, user)

            messages.success(
                request,
                f"Bienvenue {user.username}"
            )

            return redirect(settings.LOGIN_REDIRECT_URL)

    context = {
        'login_form': login_form,
        'register_form': register_form,
        'mode': mode
    }

    return render(request, 'comptes/auth.html', context)


def dashboard_view(request):

    profil, _ = Profil.objects.get_or_create(user=request.user)

    cv = CV.objects.filter(profil=profil).first()
    return render(request, 'comptes/dashboard.html', {
        "cv": cv,
        "profil": profil
    })

FORMS = [
    ("profil", ProfilForm),
    ("diplome", DiplomeForm),
    ("experience", ExperienceForm),
    ("competence", CompetenceForm),
]

wizard_storage = FileSystemStorage(location='media/temp')

class OnboardingWizard(SessionWizardView):
    form_list = FORMS
    template_name = "comptes/onboarding.html"

    file_storage = wizard_storage

    def done(self, form_list, **kwargs):

        user = self.request.user
        profil = user.profil

        profil.onboarding_done = True
        profil.save()

        cv, _ = CV.objects.get_or_create(profil=profil)

        for form in form_list:

            # ===== PROFIL =====
            if isinstance(form, ProfilForm):
                
                data = form.cleaned_data

                profil.nom = data["nom"]
                profil.prenom = data["prenom"]
                profil.telephone = data["telephone"]
                profil.adresse = data["adresse"]
                profil.bio = data["bio"]
                profil.photo = data["photo"]

                profil.save()

            # ===== DIPLOME =====
            elif isinstance(form, DiplomeForm):

                if form.has_changed():
                    obj = form.save(commit=False)
                    obj.cv = cv
                    obj.save()

            # ===== EXPERIENCE =====
            elif isinstance(form, ExperienceForm):

                if form.has_changed():
                    obj = form.save(commit=False)
                    obj.cv = cv
                    obj.save()

            # ===== COMPETENCE =====
            elif isinstance(form, CompetenceForm):
                cv.competences.set(form.cleaned_data["competences"])

        return redirect("dashboard")