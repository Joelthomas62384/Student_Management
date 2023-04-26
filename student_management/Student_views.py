from django.shortcuts import render,redirect
from app.models import Student_leave,Student_Notification,Student,Attendance
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required(login_url="/")
def HOME(request):
    if request.user.user_type != "3":

        messages.error(request,"No Permission to go there")
        return redirect('logout')
        
    else:
        user = request.user.id
        student = Student.objects.get(admin=user)
        attendance_present = Attendance.objects.filter(status="present", student_id=student).count()
        attendance_absent = Attendance.objects.filter(student_id=student,status="absent").count()
        
        attendance_late = Attendance.objects.filter(status="late", student_id=student).count()
        
        print(student.admin.first_name)
        context = {
            "present":attendance_present,
            "absent": attendance_absent,
            "late":attendance_late
        }
        print(attendance_absent,attendance_late,attendance_present)
        return render(request,'student/student_home.html',context)

@login_required(login_url="/")
def APPLY_LEAVE(request):
    if request.user.user_type != "3":

        messages.error(request,"No Permission to go there")
        return redirect('logout')
        
    else:
        student = request.user.id
        student_id = Student.objects.get(admin=student)
        leave = Student_leave.objects.filter(student_id=student_id).order_by('-id')
        context = {
            "leave":leave
        }
        
        return render(request,"Student/apply_leave.html",context)
@login_required(login_url="/")
def APPLY_LEAVE_SAVE(request):
    if request.user.user_type != "3":

        messages.error(request,"No Permission to go there")
        return redirect('logout')
        
    else:
        if request.method =="POST":
            message = request.POST.get('message')
            date = request.POST.get('date')

            student_id = request.user.id
            student = Student.objects.get(admin=student_id)

            leave = Student_leave(student_id=student,date=date,message=message)
            leave.save()

            messages.success(request,"The Leave request has been send successfully")

            return redirect('student_apply_leave')
        



@login_required(login_url="/")
def NOTIFICATIONS(request):
    if request.user.user_type != "3":

        messages.error(request,"No Permission to go there")
        return redirect('logout')
        
    else:
        student = Student.objects.get(admin=request.user.id)
        
        notification = Student_Notification.objects.filter(student_id = student.id).order_by("-id")
        for i in notification:
            i.status=i.status+1
            i.save()

        context = {
            'notification':notification
        }
        return render(request,'Student/notifications.html',context)


@login_required(login_url="/")
def VIEW_ATTENDANCE(request):
    if request.user.user_type != "3":

        messages.error(request,"No Permission to go there")
        return redirect('logout')
        
    else:
        user = request.user.id
        attendance = Attendance.objects.filter(student_id=user).order_by("-id")
        attendance_dates = set(attendance.values_list("attandance_date", flat=True))
        attendance_dates_list = list(attendance_dates)
        print(attendance_dates_list)
        # attendance_dates_list =  attendance_dates_list.reverse()
        print(attendance_dates_list)
        print(attendance_dates)


                

        context = {
            "attendance": attendance_dates_list
        }
        return render(request, "Student/view_attendance.html", context)

@login_required(login_url="/")
def ATTENDANCE_DATE(request):
    if request.user.user_type != "3":

        messages.error(request,"No Permission to go there")
        return redirect('logout')
        
    else:
        if request.method == "POST":
            date = request.POST.get('date')
            user = request.user.id
            date_obj = datetime.strptime(date, "%B %d, %Y")
            new_date = date_obj.strftime("%Y-%m-%d")
            
            student = Student.objects.get(admin=user)
            
            attendance = Attendance.objects.filter(attandance_date=new_date,student_id=student)
            attendance_present = Attendance.objects.filter(status="present", student_id=student).count()
            attendance_all = Attendance.objects.filter(student_id=student).count()
            attendance_late = Attendance.objects.filter(status="late", student_id=student).count()
            
            attendance_late_half = attendance_late // 2  # divide by 2 to get half attendance for latecomers

            if attendance_all > 0:
                attendance_percentage = ((attendance_present + attendance_late_half) / attendance_all) * 100
            else:
                attendance_percentage = 0
            

            context = {
                "percentage":int(attendance_percentage),
                
                "attendance":attendance,
                "date":date
            }
        return render(request,"Student/date_wise.html",context)

