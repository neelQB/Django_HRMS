from django.urls import path
from attendance import views

urlpatterns=[
    path('clockin/',views.mark_checkin,name='markcheckin'),
    # path('clockout/',views.mark_checkout,name='markcheckout'),
    path('clockout/',views.test_mark_checkout,name='markcheckout'),
    path('test/',views.test,name='test'),
    path('page/',views.page,name='page'),
    path('approveleave/<int:leave_id>',views.approve_leave,name='approveleave'),
    path('rejectleave/<int:leave_id>',views.reject_leave,name='rejectleave'),

    path('punchin/', views.clock_in, name='punchin'),
    path('punchout/', views.clock_out, name='punchout'),


    path('reports/',views.reports,name='reports'),
]