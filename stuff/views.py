from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db import IntegrityError
from stuff.forms import HodProfileForm, UnitForm
from stuff.models import Department, HodProfile, Log, Program, Report, School, Unit
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from student.models import Fee, StudentProfile
from django.contrib.auth import logout

# Create your views here.

@staff_member_required(login_url='admin:login')
def create_hod_profile(request):
    context = {}
    template_name = 'stuff/create_profile.html'

    context['departments'] = Department.objects.all()
    context['schools'] = School.objects.all()

    try:
        try:
            profile_attr = HodProfile.objects.get(
                user=request.user.hodprofile.user)
        except ObjectDoesNotExist:
            if request.method == 'POST':
                form = HodProfileForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.user_id = request.user.id
                    obj.save()
                    messages.success(
                        request, f'Profile Created { request.user.username }')
                    return redirect('stuff:add_student_profile')
                else:
                    messages.warning(request, 'fill all fields')
                    return redirect('stuff:createhodprofile')
            else:
                form = HodProfileForm()
                context['form'] = form
    except IntegrityError:
        profile_attr = HodProfile.objects.get(
            user=request.user.hodprofile.user)
        messages.success(request, f'Profile Created { profile_attr }')
        return redirect('stuff:add_student_profile')

    return render(request, template_name, context)


@staff_member_required(login_url='admin:login')
def add_program_unit(request):
    context = {}
    try:
        template_name = 'stuff/unit.html'
        programs = Program.objects.filter(
            department_id=request.user.hodprofile.department_id)

        context['programs'] = programs

        if request.method == 'POST':
            form = UnitForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.program_id = request.POST.get('program')
                obj.save()
                messages.success(request, f'Unit Added Succesfully')
                return redirect('stuff:add_unit')
            else:
                messages.warning(request, f'fill all fields !!')
        else:
            form = UnitForm()
            context['form'] = form
    except ObjectDoesNotExist:
        messages.warning(request, 'Create Profile Please !!')
        return redirect('stuff:createhodprofile')
    return render(request, template_name, context)


@staff_member_required(login_url='admin:login')
def unit_scan_list(request):
    context = {}
    unit_list = Unit.objects.filter(
        program_id=request.user.hodprofile.department_id)
    template_name = 'stuff/units.html'
    context['unit_list'] = unit_list
    return render(request, template_name, context)

@staff_member_required(login_url='admin:login')
def report_list(request):
    context = {}
    template_name = 'stuff/report_list.html'
    report_list_qs = Report.objects.filter(user = request.user)
    context['report_list_qs'] = report_list_qs
    
    return render(request, template_name, context)

@staff_member_required(login_url='admin:login')
def make_student_report(request, id):
    context = {}
    log_qs = Log.objects.get(user = request.user, pk = id)
    template_name = 'stuff/report.html'
    if request.method == 'POST':
        report = Report.objects.create(
            log_id = id,
            message = request.POST.get('message'),
            user = request.user
        )
        report.save()
        
        messages.success(request, f'Report Submited successfuly {request.user}')
        return redirect('stuff:report_list  ')
    
    context['log_qs'] = log_qs
    return render(request, template_name, context)


@staff_member_required(login_url='admin:login')
def exam_attendance_register(request, id):
    context = {}
    fees = Fee.objects.all()
    template_name = 'stuff/attendance.html'
    
    get_unit_qs = Unit.objects.get(id = id)
    
    loglists = Log.objects.filter(user = request.user, unit_id = id)
    context['get_unit_qs'] = get_unit_qs
    context['loglists'] = loglists
    context['fees'] = fees
    return render(request, template_name, context)

@staff_member_required(login_url='admin:login')
def loglists(request):
    context = {}
    fees = Fee.objects.all()
    template_name = 'stuff/loglist.html'
    
    loglists = Log.objects.filter(user = request.user)
    context['loglists'] = loglists
    context['fees'] = fees
    return render(request, template_name, context)
    

@staff_member_required(login_url='admin:login')
def exam_card_scanner(request, id):
    context = {}
    unit_scan_qs = Unit.objects.get(pk=id)
    template_name = 'stuff/scan.html'

    context['unit_scan_qs'] = unit_scan_qs
    if request.method == "POST":
        
        try:
            try:
                qs = request.POST['q'].split()[4:][0]

                profile_qs = StudentProfile.objects.get(adm_number=qs)
                fee_qs = Fee.objects.get(student_id=profile_qs.id)
                log_save = Log.objects.create(
                    
                    user_id = request.user.id,
                    fee_id = fee_qs.student_id,
                    profile_id = profile_qs.id,
                    unit_id = id,
                )
                log_save.save()
                context['profile_qs'] = profile_qs
                context['fee_qs'] = fee_qs
                # create logs
            except IndexError:
                qs = request.POST['q']
                messages.warning(
                    request, f'Cannot identify the student with {qs}, Invalid exam card')
                return redirect('stuff:scan', id)
        except ObjectDoesNotExist:
            messages.warning(request, f'Cannot identify the student with {qs}, Student Not Registered')
            return redirect('stuff:scan', id)
                
        return render(request, template_name, context)
    else:
        return render(request, template_name, context)

def user_logout(request):
    logout(request)
    messages.warning(request, f'You Have logout !!!')
    return redirect('admin:login')