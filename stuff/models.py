from django.db import models
from student.models import StudentProfile, Fee
from django.contrib.auth.models import User
# Create your models here.


class School(models.Model):
    school_name = models.CharField(max_length = 191)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.school_name}'
    
class Department(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    dept_name = models.CharField(max_length = 191)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.school} : {self.dept_name}'
class Program(models.Model):
    """Model definition for Program."""
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length = 191)
    # TODO: Define fields here
    class Meta:
        """Meta definition for Program."""
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'
    def __str__(self):
        return f'{self.name}'

class Unit(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    unit_name = models.CharField(max_length = 191)
    unit_code = models.CharField(max_length = 191)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.unit_code}   {self.unit_name}'

class HodProfile(models.Model):
    """Model definition for Hod."""
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    school = models.ForeignKey(School, on_delete=models.CASCADE)   
    department = models.ForeignKey(Department, on_delete=models.CASCADE) 

    def __str__(self):
        """Unicode representation of Hod."""
        return f'{self.user}: {self.department}'
    
class Log(models.Model):
    """Model definition for Log."""

    # TODO: Define fields here
    user = models.ForeignKey(User, on_delete=models.CASCADE) #hod
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE) #student id in fee
    profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE) #student profile_id
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE) #unit id in the request variable.
    timstamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Log."""
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'

    def __str__(self):
        """Unicode representation of Log."""
        return f'{self.user}: Logs For {self.profile}'


class Report(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.log}'
    
class StudentUnit(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.student} {self.unit}'
    
class StudentProfileAttribute(models.Model):
    profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    accademic_year = models.CharField(max_length = 191)
    year_of_study = models.CharField(max_length = 191)
    student_session = models.CharField(max_length = 191)
    picture = models.FileField(upload_to='StudentProfileAttribute')
    program = models.CharField(max_length = 191) #new in mind save id of the Program Model
    timestamp = models.DateTimeField(auto_now_add=True)
    
    study_method = models.CharField(max_length = 191, default= "REGULAR", null = True)#new
    
    def __str__(self):
        return f'{self.profile} : {self.department} : {self.year_of_study} Year'
    
class ExamCardNumber(models.Model):
    """Model definition for ExamCardNumber."""
    profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    number = models.CharField(max_length = 191)
    semester = models.CharField(max_length = 191)
    accademic_year = models.CharField(max_length = 191)

    # TODO: Define fields here

    class Meta:
        """Meta definition for ExamCardNumber."""

        verbose_name = 'ExamCardNumber'
        verbose_name_plural = 'ExamCardNumbers'

    def __str__(self):
        """Unicode representation of ExamCardNumber."""
        return f'{self.profile} Exam Card Number: {self.number}'

