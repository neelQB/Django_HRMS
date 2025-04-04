import re
from email.policy import default

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.core import validators
from django.forms import EmailInput

Employee = get_user_model()

class AddEmployeeForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email Id'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    mobile = forms.CharField(validators=[validators.MaxLengthValidator(10),validators.MinLengthValidator(10)])
    dob = forms.DateField(widget=forms.DateInput(attrs={'type':'date',}))
    profile = forms.ImageField(label='Profile Picture',widget=forms.ClearableFileInput())

    class Meta:
        model = Employee
        fields = ['email','first_name','last_name','gender','dob','mobile','team','role','profile','address','is_superuser']

        def clean_first_name(self):
            valname = self.cleaned_data['first_name']
            digit_regex = '[\d|\s]'
            if re.search(digit_regex,valname):
                raise forms.ValidationError('Name must not have digits or blank spaces')

        def clean_last_name(self):
            # cleaned_data = super().clean()
            valname = self.cleaned_data['last_name']

            digit_regex = '[\d|\s]'

            if re.search(digit_regex,valname):
                raise forms.ValidationError('Name must not have digits or blank spaces')


class EditEmployeeForm(UserChangeForm):
    password = None
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email Id'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}))

    mobile = forms.CharField(validators=[validators.MaxLengthValidator(10),validators.MinLengthValidator(10)])

    dob = forms.DateField(widget=forms.DateInput(attrs={'type':'date',}))

    profile = forms.ImageField(label='Profile Picture',widget=forms.ClearableFileInput())

    class Meta:
        model = Employee
        fields = ['first_name','last_name','gender','dob','mobile','profile','address']

        def clean_first_name(self):
            valname = self.cleaned_data['first_name']

            digit_regex = '\d|\s'

            if re.search(digit_regex, valname):
                raise forms.ValidationError('Name must not have digits or blank spaces')
            return valname

        def clean_last_name(self):
            # cleaned_data = super().clean()
            valname = self.cleaned_data['last_name']

            digit_regex = '\d|\s'

            if re.search(digit_regex, valname):
                raise forms.ValidationError('Name must not have digits or blank spaces')
            return valname


class LoginEmployeeForm(AuthenticationForm):
    username = forms.EmailField(widget=EmailInput(attrs={'placeholder':'Email Id'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
