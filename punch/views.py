from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from employee.models import Employee
from punch.models import Punch
from django.utils.timezone import now


# Create your views here.
@login_required
def punch_in(request):
    employee = Employee.objects.get(request.user)
    today=now().date()
    # punch , created = Punch.objects.get_or_create(employee=employee,date=)
    return render(request,'punch/punch.html',{'today',today})