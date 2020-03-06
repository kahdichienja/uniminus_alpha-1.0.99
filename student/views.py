from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import qrcode
import json
import string_utils
from qr_code.qrcode.utils import QRCodeOptions
import random
from student.forms import UserLoginForm, UserRegisterForm, StudentProfileForm, StudentProfileAttributeForm
from student.models import Fee, StudentProfile
from stuff.models import Department, ExamCardNumber, HodProfile, Program, StudentProfileAttribute, StudentUnit, Unit

@login_required(login_url='student:login_student')
def delete_unit(request, id):
    StudentUnit.objects.get(pk=id).delete()
    messages.success(request, 'Unit Deleted Successfully')
    return redirect('student:add_unit')
    

@login_required(login_url='student:login_student')
def add_unit(request):
    context = {}
    try:
        profile_attr = StudentProfileAttribute.objects.get(profile_id = request.user.studentprofile.id)
        
        units = Unit.objects.filter(program_id = profile_attr.program)
        studentUnit_qs = StudentUnit.objects.filter(student_id = request.user.studentprofile.id)
        context['profile_attr'] = profile_attr 
        context['units'] = units  
        context['studentUnit_qs'] = studentUnit_qs
        if request.method == 'POST':
            try:
                obj = StudentUnit.objects.get(
                    student_id = request.user.studentprofile.id,
                    unit_id = request.POST.get('unit'),
                )
                messages.warning(request, f'Unit Already exist {request.user.username}')
            except StudentUnit.DoesNotExist:
                new_values = {}
                new_values.update(
                    student_id = request.POST.get('student'),
                    unit_id = request.POST.get('unit')
                )
                obj = StudentUnit(**new_values)
                obj.save()
            
            # formdata = StudentUnit.objects.create(
            #     student_id = request.POST.get('student'),
            #     unit_id = request.POST.get('unit'),
            # )
            
            
            # formdata.save()
    except ObjectDoesNotExist:
        messages.warning(request, f'Register Your Department {request.user.username}')
        return redirect('student:student_profile_attribute')
    return render(request, 'pages/unit.html', context)

@login_required(login_url='student:login_student')
def student_exam_card(request):
    context = {}
    try:
        profile_attr = StudentProfileAttribute.objects.get(profile_id = request.user.studentprofile.id)
        
        units = Unit.objects.filter(program = profile_attr.program)
        programs = Program.objects.get(id = profile_attr.program)
        studentUnit_qs = StudentUnit.objects.filter(student_id = request.user.studentprofile.id)
        context['programs'] = programs
        
        exam_card_number = string_utils.shuffle(request.user.studentprofile.adm_number)
        
        try:
            obj = ExamCardNumber.objects.get(
                profile_id = request.user.studentprofile.id,
                semester = profile_attr.student_session,
                accademic_year = profile_attr.accademic_year
            )
            context['exam_card_number'] = obj.number
        except ExamCardNumber.DoesNotExist:
            new_values = {}
            new_values.update(
                profile_id = request.user.studentprofile.id,
                number = exam_card_number, 
                semester = profile_attr.student_session,
                accademic_year = profile_attr.accademic_year
            )
            obj = ExamCardNumber(**new_values)
            obj.save()
            context['exam_card_number'] = exam_card_number
        
        fullname = f'{request.user.studentprofile.first_name} {request.user.studentprofile.surname} {request.user.studentprofile.last_name}'
        qr_metadata = f'{exam_card_number} {fullname} {request.user.studentprofile.adm_number}'
        
        context['profile_attr'] = profile_attr 
        context['units'] = units  
        context['studentUnit_qs'] = studentUnit_qs
        context['my_options'] = qr_metadata        
        
    except ObjectDoesNotExist:
        messages.warning(request, f'Register Your Department {request.user.username}')
        return redirect('student:student_profile_attribute')
    return render(request, 'pages/examcard.html', context)

@login_required(login_url='student:login_student')
def edit_student_profile(request):
    context = {}
    try:
        profile_attr = StudentProfileAttribute.objects.get(profile_id = request.user.studentprofile.id)
        context['profile_attr'] = profile_attr
        programs = Program.objects.all()
        departments = Department.objects.all()
        context['departments'] = departments
        context['programs'] = programs
        if request.method == 'POST':
            
            accademic_year = request.POST['accademic_year']
            year_of_study = request.POST['year_of_study']
            student_session = request.POST['student_session']
            
            StudentProfileAttribute.objects.filter(profile_id = request.user.studentprofile.id).update(
                accademic_year = accademic_year,
                year_of_study = year_of_study,
                student_session = student_session,
            )
            messages.success(request, f'Profile for {request.user.username} was Updated successfuly!')
            return redirect('student:edit_student_profile')    

    except ObjectDoesNotExist:
        profile_attr = StudentProfileAttribute.objects.get(profile_id = request.user.studentprofile.id)
        return redirect('student:student_profile')
    return render(request, 'pages/editprofileattr.html', context)


@login_required(login_url='student:login_student')
def student_profile(request):
    context = {}
    try:
        profile_attr = StudentProfileAttribute.objects.get(profile_id = request.user.studentprofile.id)
        year_percentage = int(profile_attr.year_of_study)/4 * 100
        
        student_unit = StudentUnit.objects.filter(student_id = request.user.studentprofile.id).count()
        units = Unit.objects.filter(program=profile_attr.program).count()
        fee_qs = Fee.objects.filter(student_id = request.user.studentprofile.id)
        
        context['units'] = units
        context['profile_attr'] = profile_attr
        context['year_percentage'] = year_percentage
        context['student_unit'] = student_unit
        context['fee_qs'] = fee_qs
        
    except ObjectDoesNotExist:
        messages.warning(request, f'Register Your Department {request.user.username}')
        return redirect('student:student_profile_attribute')    
    return render(request, 'pages/profile.html', context)

@login_required(login_url='student:login_student')
def student_profile_attribute(request):
    try:
        profile_attr = StudentProfileAttribute.objects.get(profile_id = request.user.studentprofile.id)
        return redirect('student:student_profile')
    except ObjectDoesNotExist:
        context = {}
        programs = Program.objects.all()
        departments = Department.objects.all()
        context['departments'] = departments
        context['programs'] = programs
        if request.method == 'POST':
            form = StudentProfileAttributeForm(request.POST, request.FILES)
            print(request.POST['program'])
            if form.is_valid():
                obj = form.save(commit = False)
                obj.profile_id = request.user.studentprofile.id
                obj.department_id = request.POST['department']
                obj.program = request.POST['program']
                obj.save()
                messages.success(request, f'Profile Attribute for {request.user.username} was created successfuly!')
                return redirect('student:student_profile')  
            else:
                messages.warning(request, f'Fill the form Correctly {request.user.username}')
                return redirect('student:student_profile_attribute')  
        else:
            form = StudentProfileAttributeForm()
            context['form'] = form
        return render(request, 'pages/profileattr.html', context)

def login_student(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # str_relace = str.replace(username, '/', f'')
            user = authenticate(username=username,password=password)
            login(request, user)
            messages.success(request, f'login was successful')
            return redirect('student:student_profile')
        else:
            messages.warning(request, f'login Error !!!! Provide Correct Username And Password')
            return redirect('student:login_student')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


@staff_member_required(login_url='admin:login')
def add_student_profile(request):
    try:
        profile_attr = HodProfile.objects.get(user = request.user.hodprofile.user)
        if request.method == 'POST':
            form = StudentProfileForm(request.POST)
            if form.is_valid():
                adm_number = form.cleaned_data.get('adm_number')
                email_address = form.cleaned_data.get('first_name')
                email_to_save = f'{email_address}@gmail.com'
                
                user_qs = User.objects.filter(username=adm_number)
                if user_qs.count() == 1:
                    user = user_qs.first()
                    # check if the student already exists
                    # user = authenticate(username=adm_number,password=adm_number)
                    # login(request, user)
                    messages.warning(request, f'Student with Adm No. :{adm_number}, already exist')
                    return redirect('stuff:add_student_profile')
                else:
                    User.objects.create_user(
                        username = adm_number,
                        email= email_to_save,
                        password = adm_number,
                    )
                
                    # Authenticate the created student with the profile
                    # user = authenticate(username=adm_number,password=adm_number)
                    # login(request, user)
                    set_user_id = User.objects.get(username=adm_number)
                    messages.success(request, f'{adm_number} created successful')
                    # save the StudentProfileForm with the current set user id
                    obj = form.save(commit = False)
                    obj.user_id = set_user_id.id
                    obj.save()  
                    return redirect('stuff:add_student_profile')
            else:
                messages.success(request, f'login Error !!!! Provide Correct Username And Password')
                return redirect('stuff:add_student_profile')
        else:
            form = StudentProfileForm()
        return render(request, 'stuff/addstudentprofilel.html', {'form': form})
    except ObjectDoesNotExist:
        return redirect('stuff:createhodprofile')


def user_logout(request):
    logout(request)
    messages.warning(request, f'You Have logout !!!')
    return redirect('student:login_student')