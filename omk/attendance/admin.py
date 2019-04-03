from django.contrib import admin
from .models import School, Student, Mentor, Meeting, User, Employee
from django.contrib.auth.admin import UserAdmin


# class SchoolList(admin.ModelAdmin):
#     list_display = ['school_name']
#     list_filter = ['school_name']
#     ordering = ['school_name']
#
# class StudentList(admin.ModelAdmin):
#     list_display = ('id', 'name','gender', 'email', 'school')
#     search_fields =  ('id')
#
# class  MentorList(admin.ModelAdmin):
#     list_display = ('id','name','gender', 'email')
#
# class  MeetingList(admin.ModelAdmin):
#     list_display = ('mentor', 'student', 'date','time', 'location')

#class  StudentMeetingList(admin.ModelAdmin):
#    list_display = ('student','meeting')


admin.site.register(User, UserAdmin)
admin.site.register(School)
admin.site.register(Student)
admin.site.register(Mentor)
admin.site.register(Employee)
admin.site.register(Meeting)
#admin.site.register(StudentMeeting, MeetingList)
