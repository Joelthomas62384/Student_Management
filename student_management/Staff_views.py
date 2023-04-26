from django.shortcuts import render,redirect
from app.models import Staff,Staff_Notification,Staff_leave,Subject,Session_Year,Student,Attendance,Course
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required

today = datetime.date.today()
date = today.strftime('%Y-%m-%d')


def round_to_second(dt):
    return dt.replace(microsecond=1, tzinfo=datetime.timezone.utc)


@login_required(login_url='/')
def HOME(request):
    
    if request.user.user_type != "2" or request.user.user_type != "1":

        messages.error(request,"No Permission to go there")
        return redirect('logout')
        
    else:
        context = {
            'student':Student.objects.all().count(),
            'staff':Staff.objects.all().count(),
            'course':Course.objects.all().count(),
            'subject':Subject.objects.all().count(),
            'male_student':Student.objects.filter(gender="Male").count(),
            'Female_student':Student.objects.filter(gender="Female").count()
        }
        return render(request,'Staff/Home.html',context) 




@login_required(login_url="/")
def NOTIFICATIONS(request):
    if request.user.user_type != "2" or request.user.user_type != "1":
        
        messages.error(request,"No Permission to go there")
        return redirect('logout')
        
    else:
        staff = Staff.objects.get(admin=request.user.id)
        
        notification = Staff_Notification.objects.filter(staff_id = staff.id).order_by("-id")
        for i in notification:
            i.status=i.status+1
            i.save()

        context = {
            'notification':notification
        }
        return render(request,'Staff/staff_notifications.html',context)


@login_required(login_url="/")
def APPLY_LEAVE(request):
    if request.user.user_type != "2" or request.user.user_type != "1":
        
        messages.error(request,"No Permission to go there")
        return redirect('logout')
        
    else:
        staff = request.user.id
        staff_id = Staff.objects.get(admin=staff)
        leave = Staff_leave.objects.filter(staff_id=staff_id).order_by('-id')
        context = {
            "leave":leave
        }
        # for i in leave:
        #     print(i.message)
        return render(request,"Staff/apply_leave.html",context)
@login_required(login_url="/")
def APPLY_LEAVE_SAVE(request):
    if request.user.user_type != "2" or request.user.user_type != "1":
        
        messages.error(request,"No Permission to go there")
        return redirect('logout')
        
    else:
        if request.method =="POST":
            message = request.POST.get('message')
            date = request.POST.get('date')

            staff_id = request.user.id
            staff = Staff.objects.get(admin=staff_id)

            leave = Staff_leave(staff_id=staff,date=date,message=message)
            leave.save()

            messages.success(request,"The Leave request has been send successfully")
            

            



            return redirect('staff_apply_leave')
    
@login_required(login_url="/")
def TAKE_ATTENDANCE(request):
    if request.user.user_type != "2" or request.user.user_type != "1":
        
        messages.error(request,"No Permission to go there")
        return redirect('logout')
        
    else:
        staff = Staff.objects.get(admin=request.user.id)
        subject = Subject.objects.filter(staff=staff)
        session = Session_Year.objects.all()
        course = Course.objects.all()

        action = request.GET.get('action')
        students = None
        get_subject=None
        get_session=None
        subject_id = None
        session_id = None
        course_send = None 
        
        if action is not None:
            if request.method == "POST":
                session_id = request.POST.get('session_id')
                course_id = request.POST.get('course_id')
                course_send = Course.objects.get(id = course_id)
                # course_id = Course.objects.filter(id=course_id)
                
                print(session_id)

                subject = Subject.objects.get(course=course_send)
                subject = Subject.objects.filter(course=course_send)

                get_session = Session_Year.objects.get(id=session_id)
                

            
        context = {
            'subject':subject,
            'session':session,
            'course_send':course_send,
            'get_session':get_session,
            'action':action,
            "today":date,
            "students":students,
            "subject_id":subject_id,
            "session_id":session_id,
            "course":course
            
        }

        return render(request,'Staff/take_attendance.html',context)
        

from django.shortcuts import get_object_or_404
@login_required(login_url="/")
def SAVE_ATTENDANCE(request):
    if request.user.user_type != "2" or request.user.user_type != "1":
        
        messages.error(request,"No Permission to go there")
        return redirect('logout')
        
    else:
        if request.method == "POST":
            student_ids = request.POST.getlist("student_id")
            session_id = request.POST.get('session_id')
            subject_id = request.POST.get('subject_id')
            attendance_list = [request.POST.get(f'radio_{i}') for i in student_ids]
            date = request.POST.get('date')
            course_id = request.POST.getlist("course_id")
            

            session_year = get_object_or_404(Session_Year, id=session_id)
            for i, student_id in enumerate(student_ids):
                student = get_object_or_404(Student, id=student_id)
                course_id = student.course_id.id
                course = Course.objects.get(id=course_id)
                
                attendance = Attendance(student_id=student, subject_id_id=subject_id, attandance_date=date, session_year_id=session_year, status=attendance_list[i],course=course)
                attendance.save()

            messages.success(request, "Attendance registered successfully")
            return redirect("take_attendance")

@login_required(login_url="/")
def VIEW_ATTENDANCE(request):
    if request.user.user_type != "2" or request.user.user_type != "1":
        
        messages.error(request,"No Permission to go there")
        return redirect('logout')
        
    else:
        session = Session_Year.objects.all()

        action = request.GET.get('action')
        course_id = None
        session_send= None
        attendance = None
        session_id=None
        course_send=None
        attendance_date=None
        
        if action is not None:
            if request.method=="POST":
                course_id = request.POST.get('course_id')
                session_id = request.POST.get('session_id')
                attendance_date = request.POST.get('date')
                print(attendance_date)
                session_send = Session_Year.objects.get(id=session_id)
                course = Course.objects.get(id=course_id)
            course_send = {
                'id': course.id,
                'name': course.name
            }
        attendance = set(Attendance.objects.filter(course_id=course_id, session_year_id=session_id).values_list('attandance_date', flat=True))
        
        
        
        context = {
            'session' : session,
            'course': Course.objects.all(),
            'action':action,
            "course_id":course_send,
            "session_id":session_send,
            "attendance":attendance,
            
            "subject":Subject.objects.filter(course=course_id),
            "student":Student.objects.filter(course_id=course_id,session_year_id=session_id)
        }
        
        
        return render(request,"Staff/view_attendance.html",context)

@login_required(login_url="/")
def ATTENDANCE_DATE(request):
    from datetime import datetime
    if request.user.user_type != "2" or request.user.user_type != "1":
        
        messages.error(request,"No Permission to go there")
        return redirect('logout')
        
    else:

        if request.method == "POST":
            course_id = request.POST.get("course_id")
            session_id = request.POST.get("session_id")
            date = request.POST.get("date")
            
            date_obj = datetime.strptime(date, "%B %d, %Y")
            new_date = date_obj.strftime("%Y-%m-%d")
            course = Course.objects.get(id=course_id)
            session = Session_Year.objects.get(id=session_id)
            student = Student.objects.filter(course_id=course,session_year_id=session)
            attendance = Attendance.objects.filter(course =course,session_year_id_id=session,attandance_date=new_date )

            attendance_created = set(map(round_to_second, attendance.values_list("created_at", flat=True)))

            subject_list = []


            print(subject_list)
            
            

            forrange = len(attendance)/len(student)
            forrange = int(forrange)
            context = {
                
                "astud":attendance,
                "date":date,
                "range":range(1,forrange+1),
                "student":student,
                "atcre":attendance_created,
                
            }
        return render(request,"Staff/date_wise.html",context)


@login_required(login_url="/")
def TAKE_ATTENDANCE_clear(request):
    if request.user.user_type != "2" or request.user.user_type != "1":
        
        messages.error(request,"No Permission to go there")
        return redirect('logout')
        
    else:

        if request.method == "POST":
            course_id = request.POST.get('course_id')
            session_id = request.POST.get('session_id')
            subject_id = request.POST.get('subject_id')
            
            
            course= Course.objects.get(id=course_id)
            session= Session_Year.objects.get(id=session_id)
            subject = Subject.objects.get(id=subject_id)
            student = Student.objects.filter(session_year_id=session,course_id=course)


            context = {
                'course':course,
                'session':session,
                'subject':subject,
                "student":student,
                "today":date
            }
        return render(request,"Staff/take_attendance2.html",context)