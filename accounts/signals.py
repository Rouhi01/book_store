from .models import Profile
from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])

