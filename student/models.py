from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 191)
    surname = models.CharField(max_length = 191)
    last_name = models.CharField(max_length = 191)
    adm_number = models.CharField(max_length = 191)
    
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.first_name} {self.surname} {self.last_name} {self.adm_number}'
    
class Fee(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    is_completed = models.BooleanField(blank=False, default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.student} {self.is_completed}'

    