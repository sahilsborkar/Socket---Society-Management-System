from django.db.models.signals import post_save
from .models import Society, SocietyProfile
from django.dispatch import receiver

@receiver(post_save, sender=Society)
def create_profile(sender, instance, created, **kwargs):
    if created:
        SocietyProfile.objects.create(society=instance)

@receiver(post_save, sender=Society)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()