from datetime import datetime, time, timedelta
from time import strftime

from django.db.models import Sum
from django.utils.timezone import now

from employee.models import Employee
from django.db import models

from punch.models import Punch


# Create your models here.
class Attendance(models.Model):
    ATTENDANCE_STATUS_CHOICES=[
        ('Absent','Absent'),
        ('Present','Present'),
        ('Late','Late'),
        ('Leave','Leave'),
    ]

    PUNCH_STATUS_CHOICES = [
        ('PUNCHEDIN','PUNCHEDIN'),
        ('PUNCHEDOUT','PUNCHEDOUT'),
    ]

    EFFECTIVE_WORKING_HOURS = timedelta(hours=8,minutes=30,seconds=0)
    OFFICIAL_START_TIME = datetime.strptime("10:00:00",'%H:%M:%S').time()

    attendance_status = models.CharField(max_length=15,choices=ATTENDANCE_STATUS_CHOICES, default='Absent')
    punch_status = models.CharField(max_length=15,choices=PUNCH_STATUS_CHOICES,default='PUNCHEDOUT')

    date = models.DateField(auto_now_add=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)

    punch_in = models.TimeField(default=time(0,0,0))
    punch_out = models.TimeField(default=time(0,0,0))
    # punch_in = models.DateTimeField(null=True,blank=True)
    # punch_out = models.DateTimeField(null=True,blank=True)
    working_hours = models.DurationField(null=True,blank=True)
    working_hours_today = models.DurationField(null=True,blank=True)

    def mark_punchin(self,check_in_time):
        self.punch_status = 'PUNCHEDIN'
        self.punch_in = check_in_time
        self.save()

    def mark_punchout(self,check_out_time):
        self.punch_status = 'PUNCHEDOUT'
        self.punch_out = check_out_time
        self.save()

    def get_working_hours_today(self):
        employee = Employee.objects.get(email=self.employee)
        today = now().date()
        ewh_today = Punch.objects.filter(employee=employee, date=today).aggregate(Sum('session_working_hours'))['session_working_hours__sum']
        return ewh_today

    def get_working_hours_this_week(self):
        employee = Employee.objects.get(email=self.employee)

        start_week = now().date() - timedelta(days=(now().weekday()))
        end_week = start_week + timedelta(days=6)

        working_hours_this_week = Punch.objects.filter(
            employee=employee,
            punch_in_time__date__gte = start_week,
            punch_out_time__date__lte = end_week,
        ).aggregate(Sum('session_working_hours'))['session_working_hours__sum']

        return working_hours_this_week

    def get_working_hours_this_month(self):

        start_month = now().date().replace(day=1)
        end_month = start_month.replace(month = start_month.month + 1) - timedelta(days=1)

        ewh_month = Punch.objects.filter(
            employee=self.employee,
            punch_in_time__date__gte = start_month,
            punch_out_time__date__lte = end_month,
        ).aggregate(Sum('session_working_hours'))['session_working_hours__sum']
        return ewh_month

    def mark_attendance(self,check_in_time):
        # official_start_time = datetime.strptime("10:00:00", "%H:%M:%S").time()
        # official_start_time = datetime.strptime("10:00:00", "%H:%M:%S")

        # official_starttime = time(10,00,00)

        if check_in_time > Attendance.OFFICIAL_START_TIME:
            self.attendance_status = 'Late'
        else:
            self.attendance_status = 'Present'
        self.mark_punchin(check_in_time)
        self.save()

    def mark_punchout_and_calc_wh(self, check_out_time):
        employee=Employee.objects.get(email=self.employee)
        self.mark_punchout(check_out_time)
        # today = datetime.today().date()
        # punch_in_datetime = datetime.combine(today,self.punch_in)
        # punch_out_datetime = datetime.combine(today,self.punch_out)
        #
        # self.working_hours = punch_out_datetime - punch_in_datetime
        self.working_hours_today = self.get_working_hours_today()
        # self.working_hours_today = Punch.objects.filter(employee=employee, date=today).aggregate(Sum('session_working_hours'))['session_working_hours__sum']
        self.save()

        # self.working_hours_today = Punch.objects.filter(employee=self.employee,date=datetime.today().date()).aggregate(Sum('session_working_hours'))


    def save(self,*args,**kwargs):
        if self.punch_in and self.punch_out:
            today = datetime.today().date()

            punch_in_datetime=datetime.combine(today,self.punch_in)
            punch_out_datetime=datetime.combine(today,self.punch_out)
            self.working_hours = punch_out_datetime - punch_in_datetime

            # aggregation_session_working_hours = Punch.objects.filter(employee=self,date=today).aggregate(Sum('session_working_hours'))
            # self.working_hours_today = aggregation_session_working_hours
        else:
            self.working_hours = datetime.strptime('00:00:00','%H:%M:%S').time()
            # self.working_hours = None
        super().save(*args,**kwargs)


    def new_mark_attendance(self,punch_time):
        if self.punch_status == 'PUNCHEDIN':
            self.punch_in=punch_time
        else:
            self.punch_in=punch_time
            self.punch_status = 'PUNCHEDIN'

        if punch_time > Attendance.OFFICIAL_START_TIME:
            self.attendance_status='Late'
        else:
            self.attendance_status='Present'
        self.save()

    def new_mark_punchout(self,punch_time):
        if self.punch_status == 'PUNCHEDOUT':
            pass
        elif self.punch_status == 'PUNCHEDIN':
            self.punch_out=punch_time
            self.punch_status="PUNCHEDOUT"

            date_today=datetime.today().date()
            punch_in_date=datetime.combine(date_today,self.punch_in)
            punch_out_date=datetime.combine(date_today,self.punch_out)

            self.working_hours = punch_out_date - punch_in_date
            self.save()








