# from datetime import timedelta, date, datetime
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import DurationField, Sum, Count
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.timezone import now


from attendance.models import Attendance
from leave.forms import Add_Leave_Form
from leave.models import Leave
from punch.models import Punch

Employee=get_user_model()

# Create your views here.
@login_required
def clock_in(request):
    session_email = request.session.get('email')
    if not session_email:
        return render('loginemployee')
    emp = Employee.objects.get(email=request.user)
    # punch = Punch.objects.create(employee=emp,date=now().date(),status='PUNCHEDIN',punch_in_time=now())
    # punch.log_punch_in(now())
    # return page(request)
    return mark_checkin(request)

@login_required
def clock_out(request):
    session_email = request.session.get('email')
    if not session_email:
        return render('loginemployee')
    punch = Punch.objects.filter(employee=request.user,date=now().date(),status='PUNCHEDIN')
    punch = punch.last()
    punch.log_punch_out(now())
    # return test_mark_checkout(request)
    return test_mark_checkout(request)


@login_required
def approve_leave(request,leave_id):
    leave_to_approve = Leave.objects.get(id=leave_id)

    leave_to_approve.actioned_by = request.user
    leave_to_approve.actioned_on = now()
    leave_to_approve.status = 'Approved'
    leave_to_approve.save()

    # test_mark_checkout(request)
    return page(request)

@login_required
def reject_leave(request,leave_id):
    leave_to_reject = Leave.objects.get(id=leave_id)

    leave_to_reject.actioned_by = request.user
    leave_to_reject.actioned_on = now()
    leave_to_reject.status = 'Rejected'
    leave_to_reject.save()

    # test_mark_checkout(request)
    return page(request)



@login_required
def mark_checkin(request):
    session_email = request.session.get('email',None)
    if not session_email:
        return redirect('loginemployee')

    emp = Employee.objects.get(email=request.user)
    attendance, created = Attendance.objects.get_or_create(employee=emp,date=now().date())
    attendance.mark_attendance(now().time())
    punch = Punch.objects.create(employee=emp,date=now().date(),status='PUNCHEDIN',punch_in_time=now())
    punch.log_punch_in(now())
        # attendance.mark_attendance(now())
    return page(request)


@login_required
def mark_checkout(request):
    EWH = Attendance.EFFECTIVE_WORKING_HOURS

    employee = Employee.objects.get(email=request.user)

    attendance = Attendance.objects.get(employee=employee,date=now().date())
    punch = Punch.objects.get(employee=employee,date=now().date(),status='PUNCHEDIN')
    attendance.mark_punchout_and_calc_wh(now().time())
    punch.log_punch_out(now())

    intime = attendance.punch_in
    outtime = attendance.punch_out

    aggregate_session_working_hours_for_today = attendance.working_hours_today
    aggregate_session_working_hours_for_today = str(aggregate_session_working_hours_for_today).split('.')[0]

    x = attendance.get_working_hours_this_week()
    x = str(x).split('.')[0]

    y = attendance.get_working_hours_this_month()
    y = str(y).split('.')[0]


    # time_remaining = EWH - attendance.working_hours

    # working_hours = attendance.working_hours
    working_hours = attendance.working_hours
    session_working_hours = punch.session_working_hours

    # week = datetime.datetime.weekday(now().date())
    # print(week)
    #
    # week2 = now() + timedelta(days=(6-week))
    # print(week2)

    aggregate_session_working_hours_for_week = 10

    time_remaining = attendance.EFFECTIVE_WORKING_HOURS - attendance.get_working_hours_today()
    leaving_time = now() + time_remaining
    time_remaining = str(time_remaining).split('.')[0]
    leaving_time = leaving_time.time()

    # start_week = now().date() - timedelta(days=(now().weekday()))
    # end_week = start_week + timedelta(days=6)
    # print(f'{start_week} -------- {end_week}')
    #
    # start_of_month = now().date().replace(day=1)
    # end_of_month = (start_of_month.replace(month = start_of_month.month + 1, day = 1) - timedelta(days=1))
    # print(f'{start_of_month} -------- {end_of_month}')


    # hw = Punch.objects.filter(
    #     employee=employee,
    #     punch_in_time__date__gte=startweek,
    #     punch_out_time__date__lte=endweek,
    #     date=now().today().date()
    # ).aggregate(week_total=Sum('session_working_hours'))['week_total']

    # print(hw)

    # aggregate_session_working_hours = Punch.objects.filter(employee=employee, date=datetime.datetime.today().date()).aggregate(Sum('session_working_hours'))['session_working_hours__sum']


    return render(
        request,
        'attendance/punchout.html',
        {
            'intime':intime,
            'outtime':outtime,
            'session_working_hours': session_working_hours,
            'aggregate_session_working_hours': aggregate_session_working_hours_for_today,
            'EFFECTIVE_WORKING_HOURS': attendance.EFFECTIVE_WORKING_HOURS,
            't_remaining': time_remaining,
            'leaving_time': leaving_time,
            'x': x,
            'y': y,
        }
    )


@login_required
def page(request):
    session_email = request.session.get('email',None)
    if not session_email:
        return redirect('loginemployee')

    # employee = Employee.objects.get(email = request.user)
    employee = Employee.objects.get(email = session_email)
    who = employee
    attendance = Attendance.objects.get(employee=request.user,date=now().date())
    if request.user.is_superuser == True:
        isadmin = True
        isemployee = False
    else:
        isadmin = False
        isemployee = True

    if attendance.punch_status == 'PUNCHEDIN':
        user_in = True
    else:
        user_in = False

    effective_working_hours = Attendance.EFFECTIVE_WORKING_HOURS
    # aggregate_working_hours_for_today = Attendance.objects.filter(employee_id=request.user,date=now().date()).values()[0]['working_hours_today']

    # if not user_in:
    #     aggregate_working_hours_for_today = attendance.get_working_hours_today()
    #     formatted_working_hours_for_today_string = str(aggregate_working_hours_for_today).split(".")[0]
    #
    #     working_hours_percentage = aggregate_working_hours_for_today/effective_working_hours * 100
    #     if working_hours_percentage >= 0 and working_hours_percentage <= 100:
    #         working_hours_progress = working_hours_percentage
    #     else:
    #         working_hours_progress = 0
    # else:
    #     try:
    #         aggregate_working_hours_for_today = attendance.get_working_hours_today()
    #         formatted_working_hours_for_today_string = str(aggregate_working_hours_for_today).split(".")[0]
    #
    #         working_hours_percentage = aggregate_working_hours_for_today / effective_working_hours * 100
    #         if working_hours_percentage >= 0 and working_hours_percentage <= 100:
    #             working_hours_progress = working_hours_percentage
    #         else:
    #             working_hours_progress = 0
    #     except:
    #         aggregate_working_hours_for_today = 0
    #         formatted_working_hours_for_today_string = 0
    #         working_hours_percentage = 0
    #         working_hours_progress = 0
    #         # pass
    #
    #
    #         # aggregate_working_hours_for_today = attendance.get_working_hours_today()
    #         # formatted_working_hours_for_today_string = str(aggregate_working_hours_for_today).split(".")[0]
    #         #
    #         # working_hours_percentage = aggregate_working_hours_for_today / effective_working_hours * 100
    #         # if working_hours_percentage >= 0 and working_hours_percentage <= 100:
    #         #     working_hours_progress = working_hours_percentage
    #         # else:
    #         #     working_hours_progress = 0

    aggregate_working_hours_for_today = attendance.get_working_hours_today()
    formatted_working_hours_for_today_string = str(aggregate_working_hours_for_today).split(".")[0]

    if aggregate_working_hours_for_today:
        working_hours_percentage = aggregate_working_hours_for_today/effective_working_hours * 100
    else:
        working_hours_percentage = 0

    if working_hours_percentage >= 0 and working_hours_percentage <= 100:
        working_hours_progress = working_hours_percentage
    else:
        working_hours_progress = 0


    # time remaining based on [ Attendance.EFFECTIVE_WORKING_HOURS - working_hours ]
    working_hours_today = attendance.get_working_hours_today()
    if working_hours_today is None:
        # working_hours_today__ = datetime.strptime('00:00:00','%H:%M:%S') + timedelta(seconds=1)
        working_hours_today = timedelta(hours=0,minutes=0,seconds=0)
    time_remaining = attendance.EFFECTIVE_WORKING_HOURS - working_hours_today
    formatted_time_remaining_string = str(time_remaining).split('.')[0]
    working_hours_this_week = attendance.get_working_hours_this_week()
    working_hours_this_week = str(working_hours_this_week).split('.')[0]
    working_hours_this_month = attendance.get_working_hours_this_month()
    working_hours_this_month = str(working_hours_this_month).split('.')[0]

    # ATTENDANCE OVERVIEW
    all_employees = Employee.objects.all()
    employee_strength = len(Employee.objects.all())
    employee_strength_present_new = \
    Attendance.objects.filter(date=now().date(), attendance_status='Present').aggregate(Count('attendance_status'))[
        'attendance_status__count'] + \
    Attendance.objects.filter(date=now().date(), attendance_status='Late').aggregate(Count('attendance_status'))[
        'attendance_status__count']
    employee_strength_absent_new = employee_strength - employee_strength_present_new
    # employee_strength_present = len(strength_present)
    # employee_strength_absent = employee_strength - employee_strength_present
    employee_strength_present_percentage = (employee_strength_present_new / employee_strength) * 100
    employee_strength_absent_percentage = (employee_strength_absent_new / employee_strength) * 100

    # TEAM MEMBERS
    all_team_employees = Employee.objects.filter(team=employee.team)

    # LEAVE DETAILS
    apply_leave = Add_Leave_Form()
    all_leaves = Leave.objects.filter(status='Pending')

    my_applied_leaves = Leave.objects.filter(
        employee=request.user,
        status='Pending',
    )

    my_actioned_leaves = Leave.objects.filter(
        employee = request.user,
        status__in = ['Rejected','Approved'],
    )

    # return JsonResponse(request, 'attendance/test2_employee_try.html', {
    return render(request, 'attendance/test2_employee_try.html', {
    # return render(request, 'attendance/test2_common.html', {
        'who': who,
        'isadmin': isadmin,
        'isemployee': isemployee,
        'user_in' : user_in,

        'effective_working_hours': effective_working_hours,
        'aggregate_working_hours_for_today': aggregate_working_hours_for_today,
        'formatted_working_hours_for_today_string': formatted_working_hours_for_today_string,
        'working_hours_progress': working_hours_progress,
        # 'working_hours_progress' : 50,
        'time_remaining': time_remaining,
        'formatted_time_remaining_string': formatted_time_remaining_string,
        'working_hours_this_week': working_hours_this_week,
        'working_hours_this_month': working_hours_this_month,
        'employee_strength_present': employee_strength_present_new,
        'employee_strength_absent': employee_strength_absent_new,
        'employee_strength_present_percentage': employee_strength_present_percentage,
        'employee_strength_absent_percentage': employee_strength_absent_percentage,
        # Employees
        'all_employees': all_employees,
        'all_team_employees': all_team_employees,
        # Leaves
        'all_leaves': all_leaves,
        'apply_leave': apply_leave,
        'my_applied_leaves': my_applied_leaves,
        'my_actioned_leaves': my_actioned_leaves,
    })


@login_required
def test_mark_checkout(request):
    ###########################################################################################################################################################################email = request.user
    session_email = request.session.get('email')
    if not session_email:
        return redirect('loginemployee')

    if request.user.is_superuser == True:
        isadmin = True
        isemployee = False
    else:
        isadmin = False
        isemployee = True

    employee = Employee.objects.get(email=request.user)
    who = Employee.objects.get(email=request.user)
    attendance = Attendance.objects.get(employee=employee,date=now().date())
    attendance.mark_punchout_and_calc_wh(now().time())
    # punch = Punch.objects.get(employee=employee,date=now().date(),status='PUNCHEDIN')
    # punch.log_punch_out(now())

    return page(request)

    # effective_working_hours = Attendance.EFFECTIVE_WORKING_HOURS
    # # aggregate_working_hours_for_today = Attendance.objects.filter(employee_id=request.user,date=now().date()).values()[0]['working_hours_today']
    #
    # aggregate_working_hours_for_today = attendance.get_working_hours_today()
    # formatted_working_hours_for_today_string = str(aggregate_working_hours_for_today).split(".")[0]
    #
    # working_hours_percentage = aggregate_working_hours_for_today/effective_working_hours*100
    # if working_hours_percentage>=0 and working_hours_percentage <= 100:
    #     working_hours_progress = working_hours_percentage
    # else:
    #     working_hours_progress = 0
    #
    # # time remaining based on [ Attendance.EFFECTIVE_WORKING_HOURS - working_hours ]
    # time_remaining = max(attendance.EFFECTIVE_WORKING_HOURS - attendance.get_working_hours_today(), timedelta(0))
    # formatted_time_remaining_string = str(time_remaining).split('.')[0]
    # working_hours_this_week = attendance.get_working_hours_this_week()
    # working_hours_this_week = str(working_hours_this_week).split('.')[0]
    # working_hours_this_month = attendance.get_working_hours_this_month()
    # working_hours_this_month = str(working_hours_this_month).split('.')[0]
    #
    # # ATTENDANCE OVERVIEW
    # all_employees = Employee.objects.all()
    # employee_strength = len(Employee.objects.all())
    # employee_strength_present_new = Attendance.objects.filter(date=now().date(),attendance_status='Present').aggregate(Count('attendance_status'))['attendance_status__count'] + Attendance.objects.filter(date=now().date(),attendance_status='Late').aggregate(Count('attendance_status'))['attendance_status__count']
    # employee_strength_absent_new = employee_strength - employee_strength_present_new
    # # employee_strength_present = len(strength_present)
    # # employee_strength_absent = employee_strength - employee_strength_present
    # employee_strength_present_percentage = (employee_strength_present_new/employee_strength)*100
    # employee_strength_absent_percentage = (employee_strength_absent_new/employee_strength)*100
    #
    # # TEAM MEMBERS
    # all_team_employees = Employee.objects.filter(team=employee.team)
    #
    # # LEAVE DETAILS
    # apply_leave = Add_Leave_Form()
    # all_leaves = Leave.objects.filter(status='Pending')
    #
    # my_applied_leaves = Leave.objects.filter(
    #     employee = request.user,
    #     status = 'Pending',
    # )
    #
    # return render(request,'attendance/test2_employee_try.html',{
    #     'who' : who,
    #     'isadmin' : isadmin,
    #     'isemployee' : isemployee,
    #     'effective_working_hours' : effective_working_hours,
    #     'aggregate_working_hours_for_today' : aggregate_working_hours_for_today,
    #     'formatted_working_hours_for_today_string' : formatted_working_hours_for_today_string,
    #     'working_hours_progress' : working_hours_progress,
    #     # 'working_hours_progress' : 50,
    #     'time_remaining' : time_remaining,
    #     'formatted_time_remaining_string' : formatted_time_remaining_string,
    #     'working_hours_this_week' : working_hours_this_week,
    #     'working_hours_this_month' : working_hours_this_month,
    #     'employee_strength_present' : employee_strength_present_new,
    #     'employee_strength_absent' : employee_strength_absent_new,
    #     'employee_strength_present_percentage' : employee_strength_present_percentage,
    #     'employee_strength_absent_percentage' : employee_strength_absent_percentage,
    #     # Employees
    #     'all_employees' : all_employees,
    #     'all_team_employees' : all_team_employees,
    #     #Leaves
    #     'all_leaves' : all_leaves,
    #     'apply_leave' : apply_leave,
    #     'my_applied_leaves' : my_applied_leaves,
    # })
    ###########################################################################################################################################################################


@login_required
def test(request):
    ######################################################################################################

    # employee_strength = len(Employee.objects.all())
    # strength_present = Attendance.objects.filter(punch_status="PUNCHEDIN")
    # employee_strength_present = len(strength_present)
    # return render(request,'attendance/test.html',{
    #     'employee_strength_present' : employee_strength_present,
    #     'employee_strength' : employee_strength,
    # })

    ######################################################################################################
    email = request.user
    employee = Employee.objects.get(email=request.user)
    who = Employee.objects.get(email=email)
    attendance = Attendance.objects.get(employee=employee,date=now().date())

    if request.user.is_superuser == True:
        isadmin = True
        isemployee = False
    else:
        isadmin = False
        isemployee = True

    if attendance.punch_status == 'PUNCHEDIN':
        user_in = True
    else:
        user_in = False


    effective_working_hours = Attendance.EFFECTIVE_WORKING_HOURS
    # aggregate_working_hours_for_today = Attendance.objects.filter(employee_id=request.user,date=now().date()).values()[0]['working_hours_today']

    aggregate_working_hours_for_today = attendance.get_working_hours_today()
    formatted_working_hours_for_today_string = str(aggregate_working_hours_for_today).split(".")[0]

    working_hours_percentage = aggregate_working_hours_for_today/effective_working_hours*100
    if working_hours_percentage>=0 and working_hours_percentage <= 100:
        working_hours_progress = working_hours_percentage
    else:
        working_hours_progress = 0

    # time remaining based on [ Attendance.EFFECTIVE_WORKING_HOURS - working_hours ]
    time_remaining = attendance.EFFECTIVE_WORKING_HOURS - attendance.get_working_hours_today()
    formatted_time_remaining_string = str(time_remaining).split('.')[0]
    working_hours_this_week = attendance.get_working_hours_this_week()
    working_hours_this_week = str(working_hours_this_week).split('.')[0]
    working_hours_this_month = attendance.get_working_hours_this_month()
    working_hours_this_month = str(working_hours_this_month).split('.')[0]

    # ATTENDANCE OVERVIEW
    all_employees = Employee.objects.all()
    employee_strength = len(Employee.objects.all())
    employee_strength_present_new = Attendance.objects.filter(date=now().date(),attendance_status='Present').aggregate(Count('attendance_status'))['attendance_status__count'] + Attendance.objects.filter(date=now().date(),attendance_status='Late').aggregate(Count('attendance_status'))['attendance_status__count']
    employee_strength_absent_new = employee_strength - employee_strength_present_new
    # employee_strength_present = len(strength_present)
    # employee_strength_absent = employee_strength - employee_strength_present
    employee_strength_present_percentage = (employee_strength_present_new/employee_strength)*100
    employee_strength_absent_percentage = (employee_strength_absent_new/employee_strength)*100

    # TEAM MEMBERS
    all_team_employees = Employee.objects.filter(team=employee.team)
    # LEAVE DETAILS
        #APPLY LEAVE
    apply_leave = Add_Leave_Form()
    all_leaves = Leave.objects.all()
    my_applied_leaves = Leave.objects.filter(
        employee = request.user,
        status = 'Pending',
    )

    return render(request,'attendance/test2_employee_try.html',{
        'who' : who,
        'isadmin' : isadmin,
        'isemployee' : isemployee,
        'effective_working_hours' : effective_working_hours,
        'aggregate_working_hours_for_today' : aggregate_working_hours_for_today,
        'formatted_working_hours_for_today_string' : formatted_working_hours_for_today_string,
        'working_hours_progress' : working_hours_progress,
        # 'working_hours_progress' : 50,
        'time_remaining' : time_remaining,
        'formatted_time_remaining_string' : formatted_time_remaining_string,
        'working_hours_this_week' : working_hours_this_week,
        'working_hours_this_month' : working_hours_this_month,
        'employee_strength_present' : employee_strength_present_new,
        'employee_strength_absent' : employee_strength_absent_new,
        'employee_strength_present_percentage' : employee_strength_present_percentage,
        'employee_strength_absent_percentage' : employee_strength_absent_percentage,
        'all_employees' : all_employees,
        'all_team_employees' : all_team_employees,
        #Leaves
        'all_leaves' : all_leaves,
        'apply_leave' : apply_leave,
        'my_applied_leaves': my_applied_leaves,
    })



def reports(request):
    return render(request, 'test2_reports.html')