from django.urls import path
from employee import views

urlpatterns=[
    # path('add/',views.add_employee,name='addemployee'),
    path('add/',views.add_employee,name='addemployee'),
    # path('login/',views.login_employee,name='loginemployee'),
    path('',views.login_employee,name='loginemployee'),
    path('dashboard/',views.dashboard_employee,name='dashboard'),
    path('logout/',views.logout_employee,name='logoutemployee'),
    path('empdetails/<int:user_id>',views.emp_details,name='empdetails'),
]