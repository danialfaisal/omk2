from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('attendance.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='attendance/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='attendance/logout.html'), name='logout'),

]
