from django.contrib import admin
from .models import Profil

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'adresse', 'telephone')
    search_fields = ('user__username', 'adresse', 'telephone')
    list_filter = ('adresse',)