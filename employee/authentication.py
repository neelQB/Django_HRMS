from django.contrib.auth.backends import BaseBackend
from employee.models import Employee


class EmailAuthBackend(BaseBackend):
    def authenticate(self,request,email=None,password=None,**kwargs):
        try:
            employee = Employee.objects.get(email=email)
            if employee.check_password(password):
                return employee
        except Employee.DoesNotExist:
            return None

    def get_employee(self,email):
        try:
            return Employee.objects.get(email=email)
        except Employee.DoesNotExist:
            return None