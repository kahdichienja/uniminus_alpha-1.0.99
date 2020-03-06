from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from . models import StudentProfile

# @receiver(pre_save, sender = StudentProfile)
# def  create_user_before_profile(sender, instance, created, **kwargs):
#     if created:
#         User.objects.create_user(instance)
        

# @receiver(pre_save, sender = StudentProfile)
# def  create_user_before_profile(sender, instance, **kwargs):
#     instance.user.save()