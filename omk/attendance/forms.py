from django import forms
from .models import Semester, Mentor, Student, Assign, AssignTime, Level, Grade


class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = ('id', 'level',)


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ('id', 'name',)

class MentorForm(forms.ModelForm):
   class Meta:
       model = Mentor
       fields = ('user', 'id', 'name', 'gender', 'email',)

class StudentForm(forms.ModelForm):
   class Meta:
       model = Student
       fields = ('level_id', 'USN', 'name', 'gender', 'email',)


class AssignForm(forms.ModelForm):
   class Meta:
       model = Assign
       fields = ('level_id', 'mentor',)

class AssignTimeForm(forms.ModelForm):
   class Meta:
       model = AssignTime
       fields = ('assign', 'period','day',)


class GradeForm(forms.ModelForm):
   class Meta:
       model = Grade
       fields = ('student', 'semester', 'grades',)