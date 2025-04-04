from traceback import print_tb

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from attendance.models import Attendance
from attendance.views import mark_checkin, page
from employee.models import Employee
from django.utils.timezone import now
from django.contrib import messages
from employee.forms import AddEmployeeForm, LoginEmployeeForm, EditEmployeeForm
from punch.models import Punch


# Create your views here.

@login_required
def add_employee(request):
    if request.method == 'POST':
        fm=AddEmployeeForm(request.POST, request.FILES)
        if fm.is_valid():
            fm.save()
            # return redirect('loginemployee')
            return redirect('page')
        else:
            print('invalid')
            print(fm.errors)
    fm=AddEmployeeForm()
    return render(request,'employee/signup.html',{'form':fm})

def logout_employee(request):
    session_email = request.session.get('email')
    if not session_email:
        return redirect('loginemployee')
    employee = Employee.objects.get(email=request.user)
    attendance = Attendance.objects.get(employee=employee,date=now().date())
    # punch = Punch.objects.filter(employee=employee, date=now().date(), status='PUNCHEDIN').last()
    punch = Punch.objects.filter(employee=employee, date=now().date(), status='PUNCHEDIN').last()
    attendance.mark_punchout_and_calc_wh(now().time())
    if punch:
        punch.log_punch_out(now())
    logout(request)
    # request.session.flush()
    return redirect('loginemployee')


def login_employee(request):
    if request.method == 'POST':
        fm=LoginEmployeeForm(data=request.POST)
        if fm.is_valid():
            email=fm.cleaned_data['username']
            password=fm.cleaned_data['password']

            user=authenticate(request,email=email,password=password)

            if user is not None:
                login(request,user)

                request.session['email']=email

                # return redirect('dashboard')
                return redirect('markcheckin')
                # return redirect('page')

    else:
        fm=LoginEmployeeForm()
    return render(request,'employee/signin.html',{'form':fm})
    # return render(request,'attendance//signin.html',{'form':fm})

# def login_employee(request):
#     if request.method == 'POST':
#         fm = LoginEmployeeForm(data=request.POST)
#         if fm.is_valid():
#             email = fm.cleaned_data['email']
#             password = fm.cleaned_data['password']
#
#             user = authenticate(request, email=email, password=password)
#
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, "Login successful! You have been checked in.")
#
#                 return redirect('markcheckin')
#             else:
#                 messages.error(request, "Invalid email or password. Please try again.")
#
#     else:
#         fm = LoginEmployeeForm()
#
#     return render(request, 'employee/signin.html', {'form': fm})


@login_required
def emp_details(request,user_id):
    emp = Employee.objects.get(id=user_id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            # emp_form = EditEmployeeForm(data=request.POST, instance=request.user)
            emp_form = EditEmployeeForm(data=request.POST, instance=emp)
            if emp_form.is_valid():
                emp_form.save()
                return page(request)
        else:
            # emp_form = EditEmployeeForm(instance=request.user)
            emp_form = EditEmployeeForm(instance=emp)
        # emp_form=AddEmployeeForm(instance=user)

        return render(request,'employee/employee_details.html',{'form':emp_form})
    else:
        return redirect('loginemployee')





@login_required
def dashboard_employee(request):
    email=request.user
    who=Employee.objects.get(email=email)

    if request.user.is_superuser:
        whoami = 'admin'
    else:
        whoami =  'employee'

    if whoami=='admin':
        employees=Employee.objects.all()
    else:
        employees=None

    return render(request, 'employee/dashboard.html',{'whoami':whoami,'who':who,'employees':employees})
    # return render(request, 'employee/dashboard_base.html',{'whoami':whoami,'who':who,'employees':employees})
    # return render(request, 'employee/main_dashboard_webcrumbs.html',{'whoami':whoami,'who':who,'employees':employees})