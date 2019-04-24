from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Semester, Mentor, Employee, Student, Attendance, Assign, time_slots, DAYS_OF_WEEK, AssignTime, AttendanceClass, AttendanceTotal, Level, Grade
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import redirect




@login_required
def index(request):
    if request.user.is_mentor:
        return render(request, 'attendance/m_homepage.html')
    if request.user.is_employee:
        return render(request, 'attendance/e_homepage.html')
    return render(request, 'attendance/logout.html')


@login_required()
def attendance(request, stud_id):
    stud = Student.objects.get(USN=stud_id)
    ass_list = Assign.objects.filter(level_id_id=stud.class_id)
    att_list = []
    for ass in ass_list:
        try:
            a = AttendanceTotal.objects.get(student=stud, semester=ass.semester)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=stud, semester=ass.semester)
            a.save()
        att_list.append(a)
    return render(request, 'attendance/attendance.html', {'att_list': att_list})


@login_required()
def attendance_detail(request, stud_id, semester_id):
    stud = get_object_or_404(Student, USN=stud_id)
    cr = get_object_or_404(Semester, id=semester_id)
    att_list = Attendance.objects.filter(semester=cr, student=stud).order_by('date')
    return render(request, 'attendance/att_detail.html', {'att_list': att_list, 'cr': cr})



# TEACHER VIEWS
@login_required
def t_clas(request, mentor_id, choice):
    teacher1 = get_object_or_404(Mentor, id=mentor_id)
    return render(request, 'attendance/t_clas.html', {'teacher1': teacher1, 'choice': choice})


@login_required()
def t_student(request, assign_id):
    ass = Assign.objects.get(id=assign_id)
    att_list = []
    for stud in ass.level_id.student_set.all():
        try:
            a = AttendanceTotal.objects.get(student=stud, semester=ass.semester)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=stud, semester=ass.semester)
            a.save()
        att_list.append(a)
    return render(request, 'attendance/t_students.html', {'att_list': att_list})


@login_required()
def t_class_date(request, assign_id):
    now = timezone.now()
    ass = get_object_or_404(Assign, id=assign_id)
    att_list = ass.attendanceclass_set.filter(date__lte=now).order_by('-date')
    return render(request, 'attendance/t_class_date.html', {'att_list': att_list})


@login_required()
def cancel_class(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    assc.status = 2
    assc.save()
    return HttpResponseRedirect(reverse('attendance:t_class_date', args=(assc.assign_id,)))


@login_required()
def t_attendance(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    ass = assc.assign
    c = ass.level_id
    context = {
        'ass': ass,
        'c': c,
        'assc': assc,
    }
    return render(request, 'attendance/t_attendance.html', context)


@login_required()
def edit_att(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    cr = assc.assign.semester
    att_list = Attendance.objects.filter(attendanceclass=assc, semester=cr)
    context = {
        'assc': assc,
        'att_list': att_list,
    }
    return render(request, 'attendance/t_edit_att.html', context)


@login_required()
def confirm(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    ass = assc.assign
    cr = ass.semester
    cl = ass.level_id
    for i, s in enumerate(cl.student_set.all()):
        status = request.POST[s.USN]
        if status == 'present':
            status = 'True'
        else:
            status = 'False'
        if assc.status == 1:
            try:
                a = Attendance.objects.get(semester=cr, student=s, date=assc.date, attendanceclass=assc)
                a.status = status
                a.save()
            except Attendance.DoesNotExist:
                a = Attendance(semester=cr, student=s, status=status, date=assc.date, attendanceclass=assc)
                a.save()
        else:
            a = Attendance(semester=cr, student=s, status=status, date=assc.date, attendanceclass=assc)
            a.save()
            assc.status = 1
            assc.save()

    return HttpResponseRedirect(reverse('attendance:t_class_date', args=(ass.id,)))


@login_required()
def t_attendance_detail(request, stud_id, semester_id):
    stud = get_object_or_404(Student, USN=stud_id)
    cr = get_object_or_404(Semester, id=semester_id)
    att_list = Attendance.objects.filter(semester=cr, student=stud).order_by('date')
    return render(request, 'attendance/t_att_detail.html', {'att_list': att_list, 'cr': cr})


@login_required()
def change_att(request, att_id):
    a = get_object_or_404(Attendance, id=att_id)
    a.status = not a.status
    a.save()
    return HttpResponseRedirect(reverse('attendance:t_attendance_detail', args=(a.student.USN, a.semester_id)))


@login_required()
def grade(request, assign_id):
    ass = Assign.objects.get(id=assign_id)
    semester = ass.semester_id
    sc_list = Grade.objects.filter(semester_id=semester)
    return render(request, 'attendance/t_grades.html', {'sc_list': sc_list})

# @login_required()
# def t_report(request, assign_id):
#     ass = get_object_or_404(Assign, id=assign_id)
#     sc_list = []
#     for stud in ass.level_id.student_set.all():
#         a = Grade.objects.get(student=stud, semester=ass.semester)
#         sc_list.append(a)
#     return render(request, 'attendance/t_report.html', {'sc_list': sc_list})


# EMPLOYEE VIEWS

# LEVEL
def level_list(request):
    levels = Level.objects.filter()
    return render(request, 'attendance/level_list.html',
                 {'levels': levels})

def level_new(request):
   if request.method == "POST":
       form = LevelForm(request.POST)
       if form.is_valid():
           level = form.save(commit=False)
           level.created_date = timezone.now()
           level.save()
           levels = Level.objects.filter()
           return render(request, 'attendance/level_list.html',
                         {'levels': levels})
   else:
       form = LevelForm()
       # print("Else")
   return render(request, 'attendance/level_new.html', {'form': form})

def level_edit(request, pk):
    level = get_object_or_404(Level, pk=pk)
    if request.method == "POST":
        # update
        form = LevelForm(request.POST, instance=level)
        if form.is_valid():
            level = form.save(commit=False)
            level.updated_date = timezone.now()
            level.save()
            levels = Level.objects.filter()
            return render(request, 'attendance/level_list.html',
                          {'levels': levels})
    else:
        # edit
        form = LevelForm(instance=level)
    return render(request, 'attendance/level_edit.html', {'form': form})

def level_delete(request, pk):
    level = get_object_or_404(Level, pk=pk)
    level.delete()
    return redirect('attendance:level_list')



# SEMESTER
def semester_list(request):
    semesters = Semester.objects.filter()
    return render(request, 'attendance/semester_list.html',
                 {'semesters': semesters})

def semester_new(request):
   if request.method == "POST":
       form = SemesterForm(request.POST)
       if form.is_valid():
           semester = form.save(commit=False)
           semester.created_date = timezone.now()
           semester.save()
           semesters = Semester.objects.filter()
           return render(request, 'attendance/semester_list.html',
                         {'semesters': semesters})
   else:
       form = SemesterForm()
       # print("Else")
   return render(request, 'attendance/semester_new.html', {'form': form})

def semester_edit(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if request.method == "POST":
        # update
        form = SemesterForm(request.POST, instance=semester)
        if form.is_valid():
            semester = form.save(commit=False)
            semester.updated_date = timezone.now()
            semester.save()
            semesters = Semester.objects.filter()
            return render(request, 'attendance/semester_list.html',
                          {'semesters': semesters})
    else:
        # edit
        form = SemesterForm(instance=semester)
    return render(request, 'attendance/semester_edit.html', {'form': form})

def semester_delete(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    semester.delete()
    return redirect('attendance:semester_list')


# MENTOR
def mentor_list(request):
    mentors = Mentor.objects.filter(created_date__lte=timezone.now())
    return render(request, 'attendance/mentor_list.html',
                 {'mentors': mentors})

def mentor_new(request):
   if request.method == "POST":
       form = MentorForm(request.POST)
       if form.is_valid():
           mentor = form.save(commit=False)
           mentor.created_date = timezone.now()
           mentor.save()
           mentors = Mentor.objects.filter(created_date__lte=timezone.now())
           return render(request, 'attendance/mentor_list.html',
                         {'mentors': mentors})
   else:
       form = MentorForm()
       # print("Else")
   return render(request, 'attendance/mentor_new.html', {'form': form})

def mentor_edit(request, pk):
    mentor = get_object_or_404(Mentor, pk=pk)
    if request.method == "POST":
        # update
        form = MentorForm(request.POST, instance=mentor)
        if form.is_valid():
            mentor = form.save(commit=False)
            mentor.updated_date = timezone.now()
            mentor.save()
            mentors = Mentor.objects.filter(created_date__lte=timezone.now())
            return render(request, 'attendance/mentor_list.html',
                          {'mentors': mentors})
    else:
        # edit
        form = MentorForm(instance=mentor)
    return render(request, 'attendance/mentor_edit.html', {'form': form})

def mentor_delete(request, pk):
    mentor = get_object_or_404(Mentor, pk=pk)
    mentor.delete()
    return redirect('attendance:mentor_list')



# STUDENT
def student_list(request):
    students = Student.objects.filter(created_date__lte=timezone.now())
    return render(request, 'attendance/student_list.html',
                 {'students': students})

def student_new(request):
   if request.method == "POST":
       form = StudentForm(request.POST)
       if form.is_valid():
           student = form.save(commit=False)
           student.created_date = timezone.now()
           student.save()
           students = Student.objects.filter(created_date__lte=timezone.now())
           return render(request, 'attendance/student_list.html',
                         {'students': students})
   else:
       form = StudentForm()
       # print("Else")
   return render(request, 'attendance/student_new.html', {'form': form})

def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        # update
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.updated_date = timezone.now()
            student.save()
            students = Student.objects.filter(created_date__lte=timezone.now())
            return render(request, 'attendance/student_list.html',
                          {'students': students})
    else:
        # edit
        form = StudentForm(instance=student)
    return render(request, 'attendance/student_edit.html', {'form': form})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('attendance:student_list')




# Assign
def assign_list(request):
    assigns = Assign.objects.filter()
    return render(request, 'attendance/assign_list.html',
                 {'assigns': assigns})

def assign_new(request):
   if request.method == "POST":
       form = AssignForm(request.POST)
       if form.is_valid():
           assign = form.save(commit=False)
           assign.created_date = timezone.now()
           assign.save()
           assigns = Assign.objects.filter()
           return render(request, 'attendance/assign_list.html',
                         {'assigns': assigns})
   else:
       form = AssignForm()
       # print("Else")
   return render(request, 'attendance/assign_new.html', {'form': form})

def assign_edit(request, pk):
    assign = get_object_or_404(Assign, pk=pk)
    if request.method == "POST":
        # update
        form = AssignForm(request.POST, instance=assign)
        if form.is_valid():
            assign = form.save(commit=False)
            assign.updated_date = timezone.now()
            assign.save()
            assigns = Assign.objects.filter()
            return render(request, 'attendance/assign_list.html',
                          {'assigns': assigns})
    else:
        # edit
        form = AssignForm(instance=assign)
    return render(request, 'attendance/assign_edit.html', {'form': form})

def assign_delete(request, pk):
    assign = get_object_or_404(Assign, pk=pk)
    assign.delete()
    return redirect('attendance:assign_list')



# AssignTime
def assigntime_list(request):
    assigntimes = AssignTime.objects.filter()
    return render(request, 'attendance/assigntime_list.html',
                 {'assigntimes': assigntimes})

def assigntime_new(request):
   if request.method == "POST":
       form = AssignTimeForm(request.POST)
       if form.is_valid():
           assigntime = form.save(commit=False)
           assigntime.created_date = timezone.now()
           assigntime.save()
           assigntimes = AssignTime.objects.filter()
           return render(request, 'attendance/assigntime_list.html',
                         {'assigntimes': assigntimes})
   else:
       form = AssignTimeForm()
       # print("Else")
   return render(request, 'attendance/assigntime_new.html', {'form': form})

def assigntime_edit(request, pk):
    assigntime = get_object_or_404(AssignTime, pk=pk)
    if request.method == "POST":
        # update
        form = AssignTimeForm(request.POST, instance=assigntime)
        if form.is_valid():
            assigntime = form.save(commit=False)
            assigntime.updated_date = timezone.now()
            assigntime.save()
            assigntimes = Assign.objects.filter()
            return render(request, 'attendance/assigntime_list.html',
                          {'assigntimes': assigntimes})
    else:
        # edit
        form = AssignTimeForm(instance=assigntime)
    return render(request, 'attendance/assigntime_edit.html', {'form': form})

def assigntime_delete(request, pk):
    assigntime = get_object_or_404(AssignTime, pk=pk)
    assigntime.delete()
    return redirect('attendance:assigntime_list')


# GRADE
def grade_list(request):
    grades = Grade.objects.filter()
    return render(request, 'attendance/grade_list.html',
                 {'grades': grades})

def grade_new(request):
   if request.method == "POST":
       form = GradeForm(request.POST)
       if form.is_valid():
           grade = form.save(commit=False)
           grade.created_date = timezone.now()
           grade.save()
           grades = Grade.objects.filter()
           return render(request, 'attendance/grade_list.html',
                         {'grades': grades})
   else:
       form = GradeForm()
       # print("Else")
   return render(request, 'attendance/grade_new.html', {'form': form})

def grade_edit(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == "POST":
        # update
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.updated_date = timezone.now()
            grade.save()
            grades = Grade.objects.filter()
            return render(request, 'attendance/grade_list.html',
                          {'grades': grades})
    else:
        # edit
        form = GradeForm(instance=grade)
    return render(request, 'attendance/grade_edit.html', {'form': form})

def grade_delete(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    grade.delete()
    return redirect('attendance:grade_list')