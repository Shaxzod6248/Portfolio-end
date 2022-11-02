from django.db.models.signals import post_save, post_delete
from django.dispatch import Signal, receiver
from django.contrib.auth.models import User
from .models import *


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        Profil.objects.create(
            user=user,
            email = user.email,
            name = user.first_name
        )


def user_edit(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.name = profile.name
        user.email = profile.email
        user.save()


def delete_user(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(create_profile, sender=User)
post_save.connect(user_edit, sender=Profil)
post_delete.connect(delete_user, sender=Profil)