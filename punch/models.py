import datetime
from tkinter.constants import CASCADE

from django.core.paginator import UnorderedObjectListWarning
from django.db import models

from employee.models import Employee


# Create your models here.


class Punch(models.Model):
    PUNCH_STATUS=[
        ('PUNCHEDIN','PUNCHEDIN'),
        ('PUNCHEDOUT','PUNCHEDOUT'),
    ]

    # id = models.IntegerField(unique=True,primary_key=True)
    status = models.CharField(max_length=20,choices=PUNCH_STATUS)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, related_name='punches')
    # employee_email=models.EmailField()
    punch_in_time = models.DateTimeField(null=True,blank=True)
    punch_out_time = models.DateTimeField(null=True,blank=True)
    date = models.DateField()
    session_working_hours = models.DurationField(null=True,blank=True)

    def log_punch_in(self,in_time):
        self.status = 'PUNCHEDIN'
        self.punch_in_time=in_time
        self.save()

    def log_punch_out(self,out_time):
        self.status = 'PUNCHEDOUT'
        self.punch_out_time=out_time
        self.save()

    def save(self,*args,**kwargs):
        if self.punch_in_time and self.punch_out_time:
            self.session_working_hours = self.punch_out_time - self.punch_in_time
        # else:
        #     self.punch_out_time = None
        super().save(*args,**kwargs)






