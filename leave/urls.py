from django.urls import path
from . import views

urlpatterns = [
    path('addleave/',views.add_leave,name='newleave'),
]