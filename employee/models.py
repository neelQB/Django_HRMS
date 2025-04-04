from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.
class EmployeeManager(BaseUserManager):
    def _create_user(self,email,password,mobile,**extra_fields):
        email=self.normalize_email(email)

        emp = self.model(email=email,password=password,mobile=mobile,**extra_fields)
        emp.set_password(password)
        emp.save(using=self._db)

    def create_user(self,email,password,mobile,**extra_fields):
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',False)

        return self._create_user(email,password,mobile,**extra_fields)

    def create_superuser(self, email,password,mobile,**extra_fields):
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        return self._create_user(email,password,mobile,**extra_fields)


class Employee(AbstractBaseUser,PermissionsMixin):
    GENDER_CHOICES=[
        ('Male','Male'),
        ('Female','Female'),
    ]

    TEAM_CHOICES=[
        ('Python','Python'),
        ('.NET','.NET'),
        ('REACT','REACT'),
    ]

    ROLE=[
        ('Manager','Manager'),
        ('Team Lead','Team Lead'),
        ('Jr. Developer','Jr. Developer'),
        ('Sr. Developer','Sr. Developer'),
        ('Intern','Intern'),
        ('Employee','Employee'),
    ]

    id = models.AutoField(unique=True,primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25,null=True,blank=True)
    gender = models.CharField(max_length=6,choices=GENDER_CHOICES,default='Male')
    mobile = models.CharField(unique=True,max_length=15)
    profile = models.ImageField(null=True,blank=True,upload_to='profilepics',default='default_profile.png')
    #
    dob = models.DateField(null=True)
    address = models.TextField(default='N.A.')
    #
    team = models.CharField(max_length=6,choices=TEAM_CHOICES)
    role = models.CharField(max_length=60,choices=ROLE,default='Employee')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    joining_date = models.DateField(auto_now_add=True)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','mobile']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
