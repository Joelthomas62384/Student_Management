"""
URL configuration for student_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import Staff_views
from . import Student_views
from . import Hod_views

urlpatterns = [
    path('admin/',admin.site.urls),
    path('',views.LOGIN,name='login'),
    path('doLogin',views.doLogin,name='doLogin'),
    path('Hod/Home',Hod_views.HOME,name='hod_home'),
    path('doLogout',views.doLogout,name='logout'),
    path('Profile',views.PROFILE,name='profile'),
    path('Profile/update',views.PROFILE_UPDATE,name='profile_update'),
    path('Hod/Student/Add',Hod_views.ADD_STUDENT,name='add_student'),
    path('Hod/Student/View',Hod_views.VIEW_STUDENT,name='view_student'),
    path('Hod/Student/Edit/<str:id>',Hod_views.EDIT_STUDENT,name='edit_student'),
    path('Hod/Student/Update',Hod_views.UPDATE_STUDENT,name='update_student'),
    path('Hod/Student/Delete/<str:admin>',Hod_views.DELETE_STUDENT,name='delete_student'),

    path('Hod/Staff/Add',Hod_views.ADD_STAFF,name='add_staff'),
    path('Hod/Staff/View',Hod_views.VIEW_STAFF,name='view_staff'),
    path('Hod/Staff/Update',Hod_views.UPDATE_STAFF,name='update_staff'),
    path('Hod/Staff/Delete/<str:admin>',Hod_views.DELETE_STAFF,name='delete_staff'),
    path('Hod/Staff/Edit/<str:id>',Hod_views.EDIT_STAFF,name='edit_staff'),

    path('Hod/Course/Add',Hod_views.ADD_COURSE,name='add_course'),
    path('Hod/Course/View',Hod_views.VIEW_COURSE,name='view_course'),
    path('Hod/Course/Edit/<str:id>',Hod_views.EDIT_COURSE,name='edit_course'),
    path('Hod/Course/Update',Hod_views.UPDATE_COURSE,name='update_course'),
    path('Hod/Course/Delete/<str:id>',Hod_views.DELETE_COURSE,name='delete_course'),

    path('Hod/Subject/Add',Hod_views.ADD_SUBJECT,name='add_subject'),
    path('Hod/Subject/View',Hod_views.VIEW_SUBJECT,name='view_subject'),
    path('Hod/Subject/Edit/<str:id>',Hod_views.EDIT_SUBJECT,name='edit_subject'),
    path('Hod/Subject/Delete/<str:id>',Hod_views.DELETE_SUBJECT,name='delete_subject'),
    path('Hod/Subject/Update',Hod_views.UPDATE_SUBJECT,name='update_subject'),


    path('Hod/Session/Add',Hod_views.ADD_SESSION,name='add_session'),
    path('Hod/Session/View',Hod_views.VIEW_SESSION,name='view_session'),
    path('Hod/Session/Edit/<str:id>',Hod_views.EDIT_SESSION,name='edit_session'),
    path('Hod/Session/Update',Hod_views.UPDATE_SESSION,name='update_session'),
    path('Hod/Session/Delete/<str:id>',Hod_views.DELETE_SESSION,name='delete_session'),
    path("Hod/Staff/Send_Staff_Notification",Hod_views.STAFF_SEND_NOTIFICATION,name='staff_send_notification'),
    path("Hod/Staff/Save_Staff_Notification",Hod_views.SAVE_STAFF_NOTIFICATION,name='save_staff_notification'),
    path("Hod/Staff/staff_notification_all",Hod_views.staff_notification_all,name='staff_notification_all'),
    path("Hod/Staff/Staff_leave",Hod_views.STAFF_LEAVE,name='staff_leave'),
    path("Hod/Staff/Staff_leave_approve/<str:id>",Hod_views.STAFF_LEAVE_APPROVE,name='staff_leave_approve'),
    path("Hod/Staff/Staff_leave_dissapprove/<str:id>",Hod_views.STAFF_LEAVE_Dis,name='staff_leave_dissapprove'),

    path("Hod/Student/Send_Student_Notification",Hod_views.STUDENT_SEND_NOTIFICATION,name='student_send_notification'),
    path("Hod/Student/student_notification_all",Hod_views.student_notification_all,name='student_notification_all'),
    path("Hod/Student/Save_student_Notification",Hod_views.SAVE_STUDENT_NOTIFICATION,name='save_student_notification'),
    path("Hod/Student/Student_leave",Hod_views.STUDENT_LEAVE,name='Student_leave'),
    path("Hod/Student/Student_leave_approve/<str:id>",Hod_views.STUDENT_LEAVE_APPROVE,name='Student_leave_approve'),
    path("Hod/Student/Student_leave_dissapprove/<str:id>",Hod_views.STUDENT_LEAVE_Dis,name='Student_leave_dissapprove'),

    #staff Panel

    path('Staff/Home',Staff_views.HOME,name="staff_home"),
    path('Staff/Notifications',Staff_views.NOTIFICATIONS,name="staff_notifications"),
    path('Staff/Apply_leave',Staff_views.APPLY_LEAVE,name="staff_apply_leave"),
    path('Staff/Apply_leave_save',Staff_views.APPLY_LEAVE_SAVE,name="staff_apply_leave_save"),
    path('Staff/Take_Attandance',Staff_views.TAKE_ATTENDANCE,name="take_attendance"),
    path('Staff/Take_Attandance2',Staff_views.TAKE_ATTENDANCE_clear,name="take_attendance2"),
    path('Staff/save_Attandance',Staff_views.SAVE_ATTENDANCE,name="save_attendance"),
    path('Staff/view_Attandance',Staff_views.VIEW_ATTENDANCE,name="view_attendance"),
    path('Staff/date_Attandance',Staff_views.ATTENDANCE_DATE,name="date_attendance"),

    # Student Panel
    path('Student/Apply_leave',Student_views.APPLY_LEAVE,name="student_apply_leave"),
    path('Student/Apply_leave_save',Student_views.APPLY_LEAVE_SAVE,name="student_apply_leave_save"),

    path('Student/Notifications',Student_views.NOTIFICATIONS,name="student_notifications"),
    path('Student/Home',Student_views.HOME,name='student_home'),
    path('Student/view_Attandance',Student_views.VIEW_ATTENDANCE,name="student_view_attendance"),
    path('Student/date_Attandance',Student_views.ATTENDANCE_DATE,name="student_date_attendance"),

]  +static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
