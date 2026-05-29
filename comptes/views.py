from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.decorators import method_decorator

from comptes.models import Profil, User
from cv.models import CV

from .forms import RegisterForm, LoginForm, ProfilForm
from cv.forms import DiplomeForm, ExperienceForm, CompetenceForm

from formtools.wizard.views import SessionWizardView

from django.http import JsonResponse
from django.views.decorators.http import require_GET

def auth_view(request):
    # Redirect authenticated users
    if request.user.is_authenticated:
        return redirect('dashboard')

    mode = request.GET.get('mode', 'login')
    login_form = LoginForm(request)
    register_form = RegisterForm()

    # ===== REGISTER =====
    if request.method == 'POST' and 'register_submit' in request.POST:
        mode = 'register'
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, "Compte créé avec succès. Connecte-toi maintenant.")
            return redirect('/auth/?mode=login')

    # ===== LOGIN =====
    elif request.method == 'POST' and 'login_submit' in request.POST:
        mode = 'login'
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)
            messages.success(request, f"Bienvenue {user.username} !")
            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'comptes/auth.html', {
        'login_form': login_form,
        'register_form': register_form,
        'mode': mode
    })


@login_required
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


@method_decorator(login_required, name='dispatch')
class OnboardingWizard(SessionWizardView):
    form_list = FORMS
    template_name = "comptes/onboarding.html"
    file_storage = wizard_storage

    def dispatch(self, request, *args, **kwargs):
        # Redirect if onboarding already done
        if request.user.is_authenticated and request.user.profil.onboarding_done:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def done(self, form_list, **kwargs):
        user = self.request.user
        profil = user.profil

        cv, _ = CV.objects.get_or_create(profil=profil)

        for form in form_list:

            # ===== PROFIL =====
            if isinstance(form, ProfilForm):
                data = form.cleaned_data
                profil.nom = data.get("nom", profil.nom)
                profil.prenom = data.get("prenom", profil.prenom)
                profil.telephone = data.get("telephone", profil.telephone)
                profil.adresse = data.get("adresse", profil.adresse)
                profil.bio = data.get("bio", profil.bio)
                if data.get("photo"):
                    profil.photo = data["photo"]

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
                cv.competences.set(form.cleaned_data.get("competences", []))

        profil.onboarding_done = True
        profil.save()

        messages.success(self.request, "Profil complété ! Ton CV est prêt. 🎉")
        return redirect("dashboard")

@require_GET
def check_username(request):
    username = request.GET.get("username", "").strip()

    if len(username) < 1:
        return JsonResponse({
            "available": False,
            "message": "Trop court"
        })
    
    exists = User.objects.filter(username=username).exists()

    return JsonResponse({
        "available": exists,
        "message": "Pris" if exists else "Disponible"
    })
