from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profil(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profil'
    )

    telephone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Numéro de téléphone de l'utilisateur"
    )

    adresse = models.TextField(
        blank=True,
        help_text="Adresse physique ou localisation"
    )

    bio = models.TextField(blank=True)

    photo = models.ImageField(
        upload_to='profils/',
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f"Profil de {self.user.username}"
    
@receiver(post_save, sender=User)
def creer_profil_utilisateur(sender, instance, created, **kwargs):

    if created:
        Profil.objects.create(user=instance)

@receiver(post_save, sender=User)
def sauvegarder_profil_utilisateur(sender, instance, **kwargs):
    
    instance.profil.save()