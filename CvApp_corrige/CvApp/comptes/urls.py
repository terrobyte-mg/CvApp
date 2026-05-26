from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from .views import auth_view, dashboard_view, OnboardingWizard

urlpatterns = [
    path('auth/', auth_view, name='auth'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('onboarding/', OnboardingWizard.as_view(), name='onboarding')
]