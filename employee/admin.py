from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.

Employee = get_user_model()


class EmployeeAdmin(UserAdmin):

    model = Employee
    readonly_fields = ['joining_date','id']
    list_display = ['id','email','first_name','mobile','is_superuser']
    ordering = ('-is_superuser',)
    fieldsets = (
        (None,{'fields':('id','email','password','mobile')}),
        ('Employee Details',{'fields':('first_name','last_name','gender','dob','address','profile')}),
        ('Team Details',{'fields':('team','role','joining_date')})
    )

    add_fieldsets = (
        (
            None,{
                'classes':('wide',),
                'fields':('email','first_name','last_name','mobile','gender','dob','address','team','role','is_active','is_staff','is_superuser')
            }
        ),
    )

admin.site.register(Employee, EmployeeAdmin)