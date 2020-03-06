from django.contrib import admin
from stuff.models import (School, HodProfile,
                          Department, Unit, Log, Report, 
                          StudentUnit, StudentProfileAttribute, 
                          Program, ExamCardNumber
)
# Register your models here.

@admin.register(HodProfile)
class HodProfileAdmin(admin.ModelAdmin):
    list_display = ["school","department","user"]


@admin.register(ExamCardNumber)
class ExamCardNumberAdmin(admin.ModelAdmin):
    pass

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ["department","name"]
    link_display = ["name"] 
    
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ["school_name"]
    link_display = ["school_name"]    
    
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["school", "dept_name"]
    link_display = ["school"]    
    
    
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ["unit_name", "unit_code", "program"]
    link_display = ["unit_name"]
    
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ["profile", "unit"]
    link_display = ["profile"]
    
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["log", "timestamp"]
    link_display = ["log"] 
    
@admin.register(StudentUnit)
class StudentUnitAdmin(admin.ModelAdmin):
    list_display = ["student", "unit"]
    link_display = ["student"]    
    
@admin.register(StudentProfileAttribute)
class StudentProfileAttributeAdmin(admin.ModelAdmin):
    list_display = ["profile","department","accademic_year","year_of_study","student_session"]
    link_display = ["profile"]
    list_filter = ["accademic_year","student_session","year_of_study"]