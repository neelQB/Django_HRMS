from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from employee.models import Employee
from leave.forms import Add_Leave_Form
from leave.models import Leave


# Create your views here.
@login_required
def add_leave(request):
    employee = Employee.objects.get(email=request.user)
    if request.method == 'POST':
        form = Add_Leave_Form(data=request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = employee
            leave.save()
            return redirect('page')
    form = Add_Leave_Form()
    return render(request,'leave/leave_form.html',{
        'form':form,
    })