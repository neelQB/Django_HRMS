from django.urls import path
from punch import views

urlpatterns=[
    path('punchin/',views.punch_in)
]