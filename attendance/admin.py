from django.contrib import admin

from attendance.models import Attendance

# Register your models here.


class AttendanceAdmin(admin.ModelAdmin):
    model = Attendance
    readonly_fields = ['working_hours','punch_in','punch_out','attendance_status']
    list_display = ['employee','date','attendance_status','punch_in','punch_out']
    ordering = ('date',)

admin.site.register(Attendance,AttendanceAdmin)