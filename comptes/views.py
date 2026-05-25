from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.conf import settings

from .forms import RegisterForm, LoginForm


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
    return render(request, 'comptes/dashboard.html')