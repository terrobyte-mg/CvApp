from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import auth_view, dashboard_view

urlpatterns = [
    path('auth/', auth_view, name='auth'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
]