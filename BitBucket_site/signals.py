from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
#from .models import UserProfile

# Connect the signal to a receiver function
###  if created:
    #    UserProfile.objects.create(user=instance)

# Connect the signal to a receiver function
#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
  #  try:
  #      profile = instance.userprofile  # Assuming you have a OneToOne relationship from User to UserProfile
   #     profile.save()
   # except UserProfile.DoesNotExist:
    #    pass