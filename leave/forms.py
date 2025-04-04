from django import forms
from django.template.context_processors import request

from employee.models import Employee
from leave.models import Leave


class Add_Leave_Form(forms.ModelForm):
    # employee=Employee.objects.get(employee=request.user)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date',}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date',}))

    # type = forms.ChoiceField
    class Meta:
        model = Leave
        fields = ['type','duration','half_day','start_date','end_date','reason']