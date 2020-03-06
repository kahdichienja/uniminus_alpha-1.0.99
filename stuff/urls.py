from django.urls import path
from student import views as student_views
from stuff import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'stuff'
urlpatterns = [
    path('', student_views.add_student_profile, name = 'add_student_profile'),
    path('create/', views.create_hod_profile, name = 'createhodprofile'),
    path('unit/add/', views.add_program_unit, name = 'add_unit'),
    path('units/', views.unit_scan_list, name = 'unit_scan_list'),    
    path('scan/<int:id>', views.exam_card_scanner, name = 'scan'),
    path('attendance/<int:id>', views.exam_attendance_register, name = 'exam_attendance_register'),
    path('logs/', views.loglists, name = 'loglists'),
    path('report/<int:id>/', views.make_student_report, name = 'make_student_report'),
    path('reports/', views.report_list, name = 'report_list'),
    path('logout/', views.user_logout, name = 'stuff_user_logout'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)