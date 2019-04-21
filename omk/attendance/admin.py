from django.contrib import admin
from .models import Semester, Student, Attendance, Mentor, Assign, AssignTime, AttendanceClass, User, Employee, Level, Grade
from django.contrib.auth.admin import UserAdmin
# Register your models here.



class StudentInline(admin.TabularInline):
    model = Student
    extra = 0


class LevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'level')
    search_fields = ('id', 'level')
    ordering = ['level']
    inlines = [StudentInline]


class SemesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    ordering = ['id']


class AssignTimeInline(admin.TabularInline):
    model = AssignTime
    extra = 0


class AssignAdmin(admin.ModelAdmin):
    inlines = [AssignTimeInline]
    list_display = ('semester_id', 'mentor')
    search_fields = ('semester_id__id', 'mentor__name')
    ordering = ['level_id__id', 'semester__id']
    raw_id_fields = ['level_id', 'semester', 'mentor']


class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'grades')
    search_fields = ('student__name', 'semester__name', 'student__level_id__id')
    ordering = ('student__level_id__id', 'student__USN')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('USN', 'name', 'level_id')
    search_fields = ('USN', 'name', 'level_id__id')


class MentorAdmin(admin.ModelAdmin):
    ordering = ['name']


admin.site.register(User, UserAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(Assign, AssignAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Employee)

