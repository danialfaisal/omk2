from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import  School, Mentor, Employee, Student, Meeting
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required



@login_required
def index(request):
    if request.user.is_mentor:
        return render(request, 'attendance/m_homepage.html')
    if request.user.is_employee:
        return render(request, 'attendance/e_homepage.html')
    return render(request, 'attendance/logout.html')


# TEACHER VIEWS
@login_required()
def t_class_date(request, mentor_id):
    mentor1 = get_object_or_404(Mentor, id=mentor_id)
    mentor1 = mentor1.meeting_set.all
    return render(request, 'attendance/t_class_date.html', {'mentor1': mentor1})


@login_required()
def cancel_class(request, ass_c_id):
    assc = get_object_or_404(Meeting, id=ass_c_id)
    assc.status = 2
    assc.save()
    return HttpResponseRedirect(reverse('t_class_date', args=(assc.mentor_id,)))


@login_required()
def t_attendance(request, meeting_id):
    mentor1 = get_object_or_404(Meeting, id=meeting_id)
    mentor1 = mentor1.student.all
    return render(request, 'attendance/t_attendance.html', {'mentor1': mentor1})


@login_required()
def edit_att(request, ass_c_id):
    assc = get_object_or_404(Meeting, id=ass_c_id)
    mentor1 = assc.student.all
    return render(request, 'attendance/t_edit_att.html', {'mentor1': mentor1,
                                                    'assc': assc})



@login_required()
def confirm(request, ass_c_id):
    assc = get_object_or_404(Meeting, id=ass_c_id)
    student = assc.student.all
    for i, s in enumerate(student):
        status = request.POST[s.id]
        if status == 'present':
            assc.attendance = 'True'
        else:
            assc.attendance = 'False'
        # if assc.status == 1:
        #     try:
        #         a = Meeting.objects.get(student=assc.student, mentor=assc.mentor, date=assc.date, time=assc.time, location=assc.location, status=assc.status)
        #         a.attendance = status
        #         a.save()
        #     except Meeting.DoesNotExist:
        #         a = Meeting(student=assc.student, mentor=assc.mentor, date=assc.date, time=assc.time, location=assc.location, status=assc.status, attendance=assc.attendance)
        #         a.save()
        # else:
        #     a = Meeting(student=assc.student, mentor=assc.mentor, date=assc.date, time=assc.time, location=assc.location, status=assc.status, attendance=assc.attendance)
        #     a.save()
        #     assc.status = 1
        #     assc.save()

    return HttpResponseRedirect(reverse('t_class_date', args=(assc.id,)))


# EMPLOYEE VIEWS





