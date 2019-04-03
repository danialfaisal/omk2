from django.db import models
import math
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from datetime import timedelta, date
from django.utils import timezone



gender = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

time_slots = (
    ('7:30 - 8:30', '7:30 - 8:30'),
    ('8:30 - 9:30', '8:30 - 9:30'),
    ('9:30 - 10:30', '9:30 - 10:30'),
    ('11:00 - 11:50', '11:00 - 11:50'),
    ('11:50 - 12:40', '11:50 - 12:40'),
    ('12:40 - 1:30', '12:40 - 1:30'),
    ('2:30 - 3:30', '2:30 - 3:30'),
    ('3:30 - 4:30', '3:30 - 4:30'),
    ('4:30 - 5:30', '4:30 - 5:30'),
)

class User(AbstractUser):
    @property
    def is_employee(self):
        if hasattr(self, 'employee'):
            return True
        return False

    @property
    def is_mentor(self):
        if hasattr(self, 'mentor'):
            return True
        return False


class School(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name




class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=50, choices=gender, default='Male')
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name





class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Student(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=20, blank=False)
    gender = models.CharField(max_length=10, choices=gender, default='Male')
    email = models.EmailField(max_length=100)
    school = models.ForeignKey(School, related_name='student_school', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.name)



class Meeting(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    student = models.ManyToManyField(Student)
    date = models.DateField()
    time = models.CharField(max_length=200, choices=time_slots)
    location = models.CharField(max_length=200)
    status = models.IntegerField(default=0)
    attendance = models.BooleanField(default='True')



    def __str__(self):
        men = Mentor.objects.get(id=self.mentor_id)
        return '%s : %s' % (men.name, self.date)





