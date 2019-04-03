from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('mentor/<slug:mentor_id>/Classes/', views.t_class_date, name='t_class_date'),
    path('mentor/<int:meeting_id>/attendance/', views.t_attendance, name='t_attendance'),
    path('mentor/<int:ass_c_id>/Cancel/', views.cancel_class, name='cancel_class'),
    path('mentor/<int:ass_c_id>/Edit_att/', views.edit_att, name='edit_att'),
    path('mentor/<int:ass_c_id>/attendance/confirm/', views.confirm, name='confirm'),


]