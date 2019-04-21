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

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)

GRADES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('F', 'F'),
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


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Semester(models.Model):
    id = models.CharField(primary_key='True', max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Level(models.Model):
    id = models.CharField(primary_key='True', max_length=100)
    level = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'levels'

    def __str__(self):
        return '%s' % self.level



class Student(models.Model):
    level_id = models.ForeignKey(Level, on_delete=models.CASCADE, default=1)
    USN = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=20, blank=False)
    gender = models.CharField(max_length=10, choices=gender, default='Male')
    email = models.EmailField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=50, choices=gender, default='Male')
    email = models.EmailField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name


class Assign(models.Model):
    level_id = models.ForeignKey(Level, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('semester', 'level_id', 'mentor'),)

    def __str__(self):
        cl = Level.objects.get(id=self.level_id_id)
        cr = Semester.objects.get(id=self.semester_id)
        te = Mentor.objects.get(id=self.mentor_id)
        return '%s : %s : %s' % (te.name, cr.name, cl)




class AssignTime(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    period = models.CharField(max_length=50, choices=time_slots, default='11:00 - 11:50')
    day = models.CharField(max_length=15, choices=DAYS_OF_WEEK)




class AttendanceClass(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.IntegerField(default=0)




class Attendance(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendanceclass = models.ForeignKey(AttendanceClass, on_delete=models.CASCADE, default=1)
    date = models.DateField(default='2018-10-23')
    status = models.BooleanField(default='True')

    def __str__(self):
        sname = Student.objects.get(name=self.student)
        cname = Semester.objects.get(name=self.semester)

        return '%s : %s' % (sname.name, cname.name)



class AttendanceTotal(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('student', 'semester'),)

    @property
    def att_class(self):
        stud = Student.objects.get(name=self.student)
        cr = Semester.objects.get(name=self.semester)
        att_class = Attendance.objects.filter(semester=cr, student=stud, status='True').count()
        return att_class

    @property
    def total_class(self):
        stud = Student.objects.get(name=self.student)
        cr = Semester.objects.get(name=self.semester)
        total_class = Attendance.objects.filter(semester=cr, student=stud).count()
        return total_class

    @property
    def attendance(self):
        stud = Student.objects.get(name=self.student)
        cr = Semester.objects.get(name=self.semester)
        total_class = Attendance.objects.filter(semester=cr, student=stud).count()
        att_class = Attendance.objects.filter(semester=cr, student=stud, status='True').count()
        if total_class == 0:
            attendance = 0
        else:
            attendance = round(att_class / total_class * 100, 2)
        return attendance

    @property
    def classes_to_attend(self):
        stud = Student.objects.get(name=self.student)
        cr = Semester.objects.get(name=self.semester)
        total_class = Attendance.objects.filter(semester=cr, student=stud).count()
        att_class = Attendance.objects.filter(semester=cr, student=stud, status='True').count()
        cta = math.ceil((0.75*total_class - att_class)/0.25)
        if cta < 0:
            return 0
        return cta



class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    grades = models.CharField(max_length=2, choices=GRADES, default='A')

    class Meta:
        unique_together = (('student', 'semester'),)
        verbose_name_plural = 'Grades'

    def __str__(self):
        sname = Student.objects.get(name=self.student)
        cname = Semester.objects.get(name=self.semester)
        return '%s : %s' % (sname.name, cname.name)

    def get_attendance(self):
        a = AttendanceTotal.objects.get(student=self.student, semester=self.semester)
        return a.attendance





def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

days = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
}


def create_attendance(sender, instance, **kwargs):
    if kwargs['created']:
        start_date = date(2019, 1, 1)
        end_date = date(2019, 12, 31)
        for single_date in daterange(start_date, end_date):
            if single_date.isoweekday() == days[instance.day]:
                try:
                    a = AttendanceClass.objects.get(date=single_date.strftime("%Y-%m-%d"), assign=instance.assign)
                except AttendanceClass.DoesNotExist:
                    a = AttendanceClass(date=single_date.strftime("%Y-%m-%d"), assign=instance.assign)
                    a.save()



post_save.connect(create_attendance, sender=AssignTime)


