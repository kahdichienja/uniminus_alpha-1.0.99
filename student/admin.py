from django.contrib import admin
from student.models import StudentProfile, Fee


# Register your models here.
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["first_name","surname", "last_name","adm_number"]
    link_display = ["adm_number"]

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ["student","is_completed"]
    link_display = ["student"]
    
