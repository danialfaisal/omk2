from django.urls import path
from . import views

app_name = 'attendance'
urlpatterns = [
    path('', views.index, name='index'),
    path('student/<slug:stud_id>/attendance/', views.attendance, name='attendance'),
    path('student/<slug:stud_id>/<slug:semester_id>/attendance/', views.attendance_detail, name='attendance_detail'),

    # Mentor URLS
    path('mentor/<slug:mentor_id>/<int:choice>/Classes/', views.t_clas, name='t_clas'),
    path('mentor/<int:assign_id>/Students/attendance/', views.t_student, name='t_student'),
    path('mentor/<int:assign_id>/ClassDates/', views.t_class_date, name='t_class_date'),
    path('mentor/<int:ass_c_id>/Cancel/', views.cancel_class, name='cancel_class'),
    path('mentor/<int:ass_c_id>/attendance/', views.t_attendance, name='t_attendance'),
    path('mentor/<int:ass_c_id>/Edit_att/', views.edit_att, name='edit_att'),
    path('mentor/<int:ass_c_id>/attendance/confirm/', views.confirm, name='confirm'),
    path('mentor/<slug:stud_id>/<slug:semester_id>/attendance/', views.t_attendance_detail, name='t_attendance_detail'),
    path('mentor/<int:att_id>/change_attendance/', views.change_att, name='change_att'),
    path('mentor/<int:assign_id>/Report/', views.t_report, name='t_report'),

    # Employee URLS

    # SEMESTER
    path('semester_list/', views.semester_list, name='semester_list'),
    path('semester/create/', views.semester_new, name='semester_new'),
    path('semester/<pk>/edit/', views.semester_edit, name='semester_edit'),
    path('semester/<pk>/delete/', views.semester_delete, name='semester_delete'),

    # LEVEL
    path('level_list/', views.level_list, name='level_list'),
    path('level/create/', views.level_new, name='level_new'),
    path('level/<pk>/edit/', views.level_edit, name='level_edit'),
    path('level/<pk>/delete/', views.level_delete, name='level_delete'),

    # MENTOR
    path('mentor_list/', views.mentor_list, name='mentor_list'),
    path('mentor/create/', views.mentor_new, name='mentor_new'),
    path('mentor/<int:pk>/edit/', views.mentor_edit, name='mentor_edit'),
    path('mentor/<int:pk>/delete/', views.mentor_delete, name='mentor_delete'),

    # STUDENT
    path('student_list/', views.student_list, name='student_list'),
    path('student/create/', views.student_new, name='student_new'),
    path('student/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('student/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Assign
    path('assign_list/', views.assign_list, name='assign_list'),
    path('assign/create/', views.assign_new, name='assign_new'),
    path('assign/<int:pk>/edit/', views.assign_edit, name='assign_edit'),
    path('assign/<int:pk>/delete/', views.assign_delete, name='assign_delete'),

    # AssignTime
    path('assigntime_list/', views.assigntime_list, name='assigntime_list'),
    path('assigntime/create/', views.assigntime_new, name='assigntime_new'),
    path('assigntime/<int:pk>/edit/', views.assigntime_edit, name='assigntime_edit'),
    path('assigntime/<int:pk>/delete/', views.assigntime_delete, name='assigntime_delete'),

    # Grade
    path('grade_list/', views.grade_list, name='grade_list'),
    path('grade/create/', views.grade_new, name='grade_new'),
    path('grade/<pk>/edit/', views.grade_edit, name='grade_edit'),
    path('grade/<pk>/delete/', views.grade_delete, name='grade_delete'),

]