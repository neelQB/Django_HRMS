from tkinter.constants import CASCADE

from django.db import models

from employee.models import Employee


# Create your models here.
class Leave(models.Model):
    LEAVE_STATUS =[
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
    ]
    LEAVE_TYPE = [
        ('Casual','Casual'),
        ('Sick','Sick'),
        ('Compensatory','Compensatory'),
    ]
    LEAVE_DURATION = [
        ('Single Day','Single Day'),
        ('Multiple Days','Multiple Days'),
        ('First Half','First Half'),
        ('Second Half','Second Half'),
    ]
    HALF_DAY_CHOICES=[
        ('None','Full Day'),
        ('First Half','First Half'),
        ('Second Half','Second Half'),
    ]

    id = models.AutoField(unique=True,primary_key=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='leaves')
    status = models.CharField(max_length=25,choices=LEAVE_STATUS,default='Pending')
    type = models.CharField(max_length=20,choices=LEAVE_TYPE)
    half_day = models.CharField(max_length=25,choices=HALF_DAY_CHOICES,default=None)
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.CharField(max_length=25,choices=LEAVE_DURATION,default='Single Day')
    reason = models.TextField()

    actioned_by=models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True)
    actioned_on = models.DateTimeField(null=True)

    # @property
    # def duration(self):
    #     if self.start_date == self.end_date and self.half_day != None:
    #         return 0.5
    #     else:
    #         return (self.end_date - self.start_date).days + 1



