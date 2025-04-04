from django.contrib import admin
from django.contrib.admin import ModelAdmin

from punch.models import Punch

# Register your models here.

class PunchAdmin(admin.ModelAdmin):

    model = Punch
    # readonly_fields = ['joining_date','id']
    list_display = ['id','date','employee','status','punch_in_time','punch_out_time','session_working_hours']
    ordering = ('-date',)
    # ordering = ('-is_superuser',)
    # fieldsets = (
    #     (None,{'fields':('id','email','password','mobile')}),
    #     ('Employee Details',{'fields':('first_name','last_name','gender','dob','address','profile')}),
    #     ('Team Details',{'fields':('team','role','joining_date')})
    # )
    #
    # add_fieldsets = (
    #     (
    #         None,{
    #             'classes':('wide',),
    #             'fields':('email','first_name','last_name','mobile','gender','dob','address','team','role','is_active','is_staff','is_superuser')
    #         }
    #     ),
    # )

admin.site.register(Punch, PunchAdmin)
