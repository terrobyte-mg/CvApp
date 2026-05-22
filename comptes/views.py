from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RegisterForm


def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Votre compte a été créé avec succès. Connectez-vous maintenant."
            )

            return redirect('login')

    else:

        form = RegisterForm()

    context = {
        'form': form
    }

    return render(request, 'comptes/register.html', context)