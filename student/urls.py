from django.urls import path
from student import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'student'
urlpatterns = [
    path('', views.login_student, name = 'login_student'),
    path('profile/', views.student_profile, name = 'student_profile'),
    path('attribute/', views.student_profile_attribute, name='student_profile_attribute'),
    path('edit/', views.edit_student_profile, name = 'edit_student_profile'),
    path('addunit/', views.add_unit, name = 'add_unit'),
    path('card/', views.student_exam_card, name = 'student_exam_card'),
    path('delete/<int:id>', views.delete_unit, name = 'delete_unit'),
    path('logout/', views.user_logout, name = 'user_logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)